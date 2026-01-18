# Core backend chatbot logic with agent-based architecture

import os
import json
from datetime import date
from amadeus import Client, ResponseError # Hotels API
from fast_flights import FlightData, Passengers, Result, get_flights # Flights API
from groq import Groq
from dotenv import load_dotenv
load_dotenv()


class Chatbot():

    def __init__(self):
        self.input_prompt = ""
        self.todays_date = date.today().isoformat()

        self.LLM_model = "llama-3.3-70b-versatile"

        self.amadeus = Client(
            client_id = os.getenv("AMADEUS_API_KEY"),
            client_secret = os.getenv("AMADEUS_API_SECRET")
        )

        # chat_history to store all of the messages in the conversation.
        # Set the system prompt to establish the behavior of the chatbot.
        self.chat_history = [
                                {"role": "system", 
                                "content": """You are a travel assistant named NaviBlu who helps provide information to users for planning trips and vacations.
                                                You can pull realtime flight and hotel information.
                                                You can also provide information about tourist attractions and activities at a location, as well as answer any general queries the user may have.
                                                You can also provide general information about travel and destinations."""}
                            ]
        # seperate history to store just the user's messages
        self.user_message_history = []

        self.flight_info = ""
        self.hotel_info = ""
        self.location_info = ""
        self.general_info = ""

        # establish Groq client for API calls
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))


    def process_input(self, input_prompt:str):
        '''Determine if the user prompt is asking for information on flights, hotels, location, or general info.'''

        print("Running process_input function")

        self.input_prompt = input_prompt
        print(f"Input prompt: {self.input_prompt}")

        # Reset info
        self.flight_info = ""
        self.hotel_info = ""
        self.location_info = ""
        self.general_info = ""

        # Add to chat history
        self.chat_history.append({"role": "user", "content": str(self.input_prompt)})
        self.user_message_history.append({"role": "user", "content": str(self.input_prompt)})
        
        # make seperate chat history just for this process
        process_input_history = [{
            "role": "system", 
            "content": """You are a classifier that determines which category of information the user needs: 'flight', 'hotel', 'location', or 'general'.
                        
                        Follow these rules:
                        - ONLY respond with one or more of these exact words: flight, hotel, location, general
                        - Separate multiple categories with commas: flight, hotel
                        - DO NOT include any other text, explanations, or examples
                        - If the user is asking about what the chatbot can do or asking meta-questions about the chatbot itself, respond ONLY with: general
                        - Only use 'location' if the user wants information about attractions and activities at a specific place
                        
                        Examples:
                        user: can you find flights to New York?
                        assistant: flight

                        user: can you find hotels in vancouver this weekend?
                        assistant: hotel

                        user: what are hotels near popular tourist locations in Orlando?
                        assistant: hotel, location

                        user: help me plan an entire trip from Charlotte to London this weekend.
                        assistant: flight, hotel, location

                        user: what are some popular activities to do in Wellington, New Zealand?
                        assistant: location

                        user: How far is Tokyo from New York?
                        assistant: general
                        
                        user: what questions can I ask?
                        assistant: general
                        
                        user: what can you do?
                        assistant: general
                        

                        """
        }]
        
        # Add all of the user's messages to process_input_history
        for message in self.chat_history:
            process_input_history.append(message)

        completion = self.client.chat.completions.create(
            model = self.LLM_model,
            messages = process_input_history, # type: ignore
            temperature = 0.0  # Set to 0 for deterministic classification
        )

        categories = str(completion.choices[0].message.content).strip().lower()
        print(f"---User Query Categories: {categories}---")
        self.user_message_history.append({"role": "assistant", "content": str(categories)}) # Add what agents were called for each query

        # Parse categories - only trigger agents if the category word appears as a standalone term
        categories_list = [cat.strip() for cat in categories.split(',')]
        
        if "flight" in categories_list:
            self.flight_info = self.flight_agent()

        if "hotel" in categories_list:
            self.hotel_info = self.hotel_agent()

        if "location" in categories_list:
            self.location_info = self.location_agent()

        if "general" in categories_list or len(categories) == 0:
            self.general_info = self.general_info_agent()
        
        # Combine the responses of all the agents
        assistant_response = f"{self.flight_info}\n{self.hotel_info}\n{self.location_info}\n{self.general_info}"

        # Add AI response to chat history
        self.chat_history.append({"role": "assistant", "content": assistant_response})

        print("Outputing Message.\n")
        return assistant_response


    def flight_agent(self):
        """Uses an LLM to parse flight parameters the user is searching for. 
        Then uses the fast-flights API to search for available flights."""

        print("Running flight agent.")

        flight_info_prompt = f"""Use this user message history to extract the flight information the user is currently looking for: 
                user message history: {self.user_message_history}
                format your response as a json exactly structured like below and nothing else. If you can't find information for a section, make an educated guess based on the message history. 
                If needed, today's date is {self.todays_date}.

                {{
                "tripType": either "round-trip" or "one-way",
                "originCity": three letter origin city iataCode,
                "destinationCity": three letter destination city iataCode,
                "originAirport": three letter origin airport code based on the city,
                "destinationAirport": three letter destination airport code based on the city,
                "departureDate": "YYY-MM-DD",
                "arrivalDate": "YYY-MM-DD" if tripType is one-way, enter "None" for this field,
                "numAdults": X If no number is specified, assume 2,
                "numChildren": X If no number is specified, assume 0,
                "seat": either "economy", "premium-economy", "business", or "first". If no specification is made, enter "economy"
                }}
                """
        
        # Use LLM to parse flight search parameters from prompt
        search_info = self.call_llm(prompt = flight_info_prompt)
        # convert to JSON
        search_info_json = json.loads(search_info) # type: ignore

        output = ["### Flight Search Parameters"]
        output.append(f"**Trip Type:** {search_info_json.get("tripType")} | **Seat:** {search_info_json.get("seat")}")
        output.append(f"**Origin:** {search_info_json.get("originCity")} ({search_info_json.get("originAirport")}) → **Destination:** {search_info_json.get("destinationCity")} ({search_info_json.get("destinationAirport")})")
        if search_info_json.get("tripType") == "one-way":
            output.append(f"**Departure:** {search_info_json.get("departureDate")}")
        else:
            output.append(f"**Departure:** {search_info_json.get("departureDate")} | **Return:** {search_info_json.get("arrivalDate")}")
        output.append(f"**Passengers:** {search_info_json.get("numAdults")} Adult(s), {search_info_json.get("numChildren")} Children\n")
        output.append("---")

        # get info for outbound flight 
        try:
            outbound: Result = get_flights(
                flight_data=[
                    FlightData(date=search_info_json.get("departureDate"), from_airport=search_info_json.get("originAirport"), to_airport=search_info_json.get("destinationAirport"))
                ],
                trip="one-way",
                seat=search_info_json.get("seat"),
                passengers=Passengers(adults=search_info_json.get("numAdults"), children=search_info_json.get("numChildren"), infants_in_seat=0, infants_on_lap=0),
                fetch_mode="fallback",
            )
        except Exception as e:
            print(f"Flight search error: {e}")
            output.append("")
            output.append("⚠️ **Unable to retrieve flight information at this time.**")
            output.append("")
            output.append("The flight search service may be temporarily unavailable.")
            output.append("Please try again later or search directly on [Google Flights](https://www.google.com/travel/flights).")
            
            output_string = ""                  
            for line in output:
                output_string += str(line) + "  \n"
            
            return str(output_string)

        output.append("### Outbound Flights")
        output.append(f"*Price Level: {outbound.current_price}*\n")

        for flight in outbound.flights:
            if flight.is_best == True:
                output.append(f"**{flight.name}** - ${flight.price}")
                output.append(f"🛫 {flight.departure} → 🛬 {flight.arrival}")
                output.append(f"⏱️ {flight.duration} | 🔄 {flight.stops} stop(s)")
                output.append("")

        # If round-trip, get info for inbound flight as well. (fast-flights API doesn't support normal round-trip)
        if search_info_json.get("tripType") == "round-trip":
            try:
                inbound: Result = get_flights(
                    flight_data=[
                        FlightData(date=search_info_json.get("arrivalDate"), from_airport=search_info_json.get("destinationAirport"), to_airport=search_info_json.get("originAirport"))
                    ],
                    trip="one-way",
                    seat=search_info_json.get("seat"),
                    passengers=Passengers(adults=search_info_json.get("numAdults"), children=search_info_json.get("numChildren"), infants_in_seat=0, infants_on_lap=0),
                    fetch_mode="fallback",
                )

                output.append("### Inbound Flights")
                output.append(f"*Price Level: {inbound.current_price}*\n")

                for flight in inbound.flights:
                    if flight.is_best == True:
                        output.append(f"**{flight.name}** - ${flight.price}")
                        output.append(f"🛫 {flight.departure} → 🛬 {flight.arrival}")
                        output.append(f"⏱️ {flight.duration} | 🔄 {flight.stops} stop(s)")
                        output.append("")
            except Exception as e:
                print(f"Inbound flight search error: {e}")
                output.append("")
                output.append("⚠️ *Unable to retrieve inbound flight information.*")

        output_string = ""                  
        for line in output:
            output_string += str(line) + "  \n"

        print("\n\nFlight Output String:\n")
        print(output_string)

        return str(output_string)


    def hotel_agent(self):
        """Uses an LLM to parse hotel search parameters the user is searching for. 
        Then uses the Amadeus API to search for available hotels."""

        print("Running hotel agent.\n")

        prompt = f"""Use this user message history to extract the hotel information the user is currently looking for: 
                user message history: {self.user_message_history}
                format your response as a json exactly structured like below and nothing else. If you can't find information for a section, make an educated guess based on the message history. 
                If needed, today's date is {self.todays_date}.

                {{
                "city": three letter city iataCode,
                "checkInDate": "YYY-MM-DD",
                "checkOutDate": "YYY-MM-DD",
                "numGuests": X  If no number is specified, assume it is 2
                }}
                """
        
        search_info = self.call_llm(prompt = prompt)
        print(search_info)
        print()

        # convert to JSON
        search_info_json = json.loads(search_info) # type: ignore
        
        try:
            # Get list of hotels by city code
            hotel_response = self.amadeus.reference_data.locations.hotels.by_city.get(cityCode=search_info_json.get("city"))

            # Make list of hotel Ids
            hotel_ids = []
            for hotel in hotel_response.data:
                hotel_ids.append(str(hotel.get("hotelId")))

            hotel_offers = self.amadeus.shopping.hotel_offers_search.get(
                hotelIds = hotel_ids[0:30], # search through first number of hotel ids
                checkInDate = search_info_json.get("checkInDate"),
                checkOutDate = search_info_json.get("checkOutDate"),
                adults = search_info_json.get("numGuests")
            )
            num_hotels = len(hotel_offers.data)
        except Exception as e:
            print(f"Hotel search error: {e}")
            output = ["### Hotel Search Parameters"]
            output.append(f"**Check-In:** {search_info_json.get('checkInDate')} | **Check-Out:** {search_info_json.get('checkOutDate')}")
            output.append(f"**City:** {search_info_json.get('city')}")
            output.append(f"**Guests:** {search_info_json.get('numGuests')}")
            output.append("")
            output.append("⚠️ **Unable to retrieve hotel information at this time.**")
            output.append("")
            output.append("The hotel search service may be temporarily unavailable or the API credentials need to be verified.")
            output.append("Please try again later or search on [Booking.com](https://www.booking.com) or [Hotels.com](https://www.hotels.com).")
            output.append("")
            output.append("---")

            output_string = ""                  
            for line in output:
                output_string += str(line) + "  \n"
            
            return str(output_string)

        if num_hotels >= 5:
            hotels_to_display = hotel_offers.data[0:5]
        elif num_hotels < 5 and num_hotels > 0:
            hotels_to_display = hotel_offers.data[0:num_hotels]
        else:
            return "Unable to find that match the search criteria."
        
        output = ["### Hotel Search Parameters"]
        output.append(f"**Check-In:** {hotels_to_display[0].get("offers")[0].get("checkInDate")} | **Check-Out:** {hotels_to_display[0].get("offers")[0].get("checkOutDate")}") # type: ignore
        output.append(f"**City:** {search_info_json.get("city")}")
        output.append("---")

        guests_info = "**Guests:** "
        guest_details = []
        for key in hotels_to_display[0].get("offers")[0].get("guests"): # type: ignore
            guest_details.append(f"{key}: {hotels_to_display[0].get("offers")[0].get("guests").get(key)}") # type: ignore
        guests_info += ", ".join(guest_details)
        output.append(guests_info)
        output.append("")

        for hotel in hotels_to_display:
            try:
                output.append("---")
                for key in hotel:
                    if key == "hotel":
                        output.append(f"### 🏨 {hotel.get(key).get("name")}") # type: ignore

                    elif key == "available":
                        availability = "✅ Available" if hotel.get(key) else "❌ Not Available"
                        output.append(f"**{availability}**") # type: ignore

                    elif key == "offers":
                        for offer in hotel.get(key): # type: ignore
                            output.append(f"**Room:** {offer.get("room").get("typeEstimated").get("category")}")
                            output.append(f"**Beds:** {offer.get("room").get("typeEstimated").get("beds")} {offer.get("room").get("typeEstimated").get("bedType")}")
                            output.append(f"**Price:** {offer.get("price").get("currency")} ${offer.get("price").get("total")} total (${offer.get("price").get("variations").get("average").get("base")}/night)")
                            output.append(f"*{offer.get("room").get("description").get("text")}*")
                output.append("")
            except Exception as e:
                print(f"Error parsing hotel info: {e}")

        output.append("")
        output_string = ""                  
        for line in output:
            output_string += str(line) + "  \n"

        print("\n\nHotel Output String:")
        print(output_string)

        return str(output_string)


    def location_agent(self):
        """Agent for answering questions about tourist attractions and activities at a location.
        Doesn't use a special API to retrieve information, just prompts the LLM for what information it has on the location."""

        print("Running location agent.")
        location_prompt = f"""Provide helpful information about tourist attractions, activities, and things to do based on this request.
        Include specific recommendations, popular landmarks, and local experiences.
        Keep your response informative but concise.
        
        User request: {self.input_prompt}"""
        response = self.call_llm(prompt = location_prompt)

        print(response)
        print()
        return response


    def general_info_agent(self):
        """Agent for answering general questions that the other agents can't answer."""

        print("Running general info agent.")
        general_prompt = f"""You are NaviBlu, a helpful travel assistant. Respond to this user query in a friendly and concise way.
        
        If the user is asking what you can do or what questions they can ask, provide a brief overview like:
        "I'm NaviBlu, your AI travel assistant! I can help you with:
        
        - ✈️ **Flight Search** - Find and compare flights for your trip
        - 🏨 **Hotel Search** - Discover hotels and accommodations  
        - 📍 **Location Info** - Learn about attractions, activities, and things to do
        - ℹ️ **General Travel Questions** - Get answers about destinations, distances, travel tips, and more
        
        Just enter questions like 'Find flights to Paris' or 'What hotels are available in Tokyo this weekend?' and I'll help you out!"
        
        Otherwise, if their question is not related to your capabilities, you should provide helpful travel-related information for their question.
        
        User query: {self.input_prompt}"""
        return self.call_llm(prompt = general_prompt)


    def call_llm(self, prompt):
        """function for LLM calls."""

        print("--Running call_llm.")

        # make chat history to send to LLM
        history = [{
                    "role": "user",
                    "content": prompt,
                    }]

        # Call LLM
        completion = self.client.chat.completions.create(
            model = self.LLM_model,
            messages = history, # type: ignore
        )

        return completion.choices[0].message.content
