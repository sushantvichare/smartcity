import json

from chatbot.router import get_current_date, get_current_hour, route_query
from chatbot.rag import retrieve_context

from chatbot.tools import (
    predict_traffic,
    predict_aqi,
    predict_complaints
)


class SmartCityAgent:

    def __init__(self, llm=None):

        self.llm = llm

    # ========================================================
    # MAIN ENTRY POINT
    # ========================================================

    def run_agent(self, query):

        try:

            # ------------------------------------------------
            # 1. ROUTE USER QUERY
            # ------------------------------------------------

            route = route_query(query)

            intent = route.get(
                "intent",
                "general"
            )

            # ------------------------------------------------
            # 2. RAG
            # ------------------------------------------------

            if intent == "rag":

                return self.handle_rag(
                    query
                )

            # ------------------------------------------------
            # 3. TRAFFIC
            # ------------------------------------------------

            elif intent == "traffic":

                return self.handle_traffic(
                    route
                )

            # ------------------------------------------------
            # 4. AQI
            # ------------------------------------------------

            elif intent == "aqi":

                return self.handle_aqi(
                    route
                )

            # ------------------------------------------------
            # 5. COMPLAINTS
            # ------------------------------------------------

            elif intent == "complaints":

                return self.handle_complaints(
                    route
                )

            # ------------------------------------------------
            # 6. GENERAL
            # ------------------------------------------------

            else:

                return self.handle_general(
                    query
                )

        except Exception as e:

            return {
                "success": False,
                "error": str(e)
            }

    # ========================================================
    # RAG HANDLER
    # ========================================================

    def handle_rag(self, query):

        context = retrieve_context(
            query
        )

        answer = self.generate_response(
            query=query,
            context=context
        )

        return {
            "success": True,
            "type": "rag",
            "answer": answer,
            "context": context
        }

    # ========================================================
    # TRAFFIC HANDLER
    # ========================================================

    def handle_traffic(self, route):

        area = route.get(
            "area"
        )

        road_name = route.get(
            "road_name"
        )

        date = route.get(
            "date"
        )

        hour = route.get(
            "hour"
        )

        weather = route.get(
            "weather",
            "Clear"
        )

        event = route.get(
            "event",
            "None"
        )

        # ----------------------------------------------
        # Validate required fields
        # ----------------------------------------------

        missing = []

        if not area:
            missing.append("area")

        if not date:
            date = get_current_date()

        if hour is None:
            hour = get_current_hour()

        if missing:

            return {
                "success": False,
                "type": "traffic",
                "requires_input": True,
                "missing": missing,
                "answer": (
                    "I need the following information "
                    "to predict traffic: "
                    + ", ".join(missing)
                )
            }

        # ----------------------------------------------
        # Call ML tool
        # ----------------------------------------------

        result = predict_traffic(
            area=area,
            road_name=road_name,
            date=date,
            hour=hour,
            weather=weather,
            event=event
        )

        if "error" in result:

            return {
                "success": False,
                "type": "traffic",
                "error": result["error"]
            }

        # ----------------------------------------------
        # Generate natural language response
        # ----------------------------------------------

        answer = self.format_model_response(
    result,
    "traffic"
)

        return {
            "success": True,
            "type": "traffic",
            "answer": answer,
            "data": result
        }

    # ========================================================
    # AQI HANDLER
    # ========================================================

    def handle_aqi(self, route):

    # ------------------------------------------------
    # DATE
    # ------------------------------------------------

        date = route.get("date")
    
        if not date:
            from datetime import datetime
            date = datetime.now().strftime("%Y-%m-%d")
    
        # ------------------------------------------------
        # TIME / HOUR
        # ------------------------------------------------
    
        hour = route.get("hour")
    
        if hour is None:
            from datetime import datetime
            hour = datetime.now().hour
    
        # ------------------------------------------------
        # Predict AQI
        # ------------------------------------------------
    
        result = predict_aqi(
            date=date
        )
    
        # ------------------------------------------------
        # Handle prediction error
        # ------------------------------------------------
    
        if "error" in result:
    
            return {
                "success": False,
                "type": "aqi",
                "error": result["error"]
            }
    
        # ------------------------------------------------
        # Generate natural language response
        # ------------------------------------------------
    
        answer = self.format_model_response(
    {
        "date": date,
        "hour": hour,
        "prediction": result
    },
    "aqi"
)
    
        # ------------------------------------------------
        # Final response
        # ------------------------------------------------
    
        return {
            "success": True,
            "type": "aqi",
            "answer": answer,
            "data": result,
            "date": date,
            "hour": hour
        }
    # ========================================================
    # COMPLAINT HANDLER
    # ========================================================

    def handle_complaints(self, route):

        required_fields = [
            "complaint_date",
            "ward_code",
            "ward_area",
            "zone",
            "ward_type",
            "population_density",
            "ward_slum_percentage",
            "complaint_category",
            "department_assigned",
            "complaint_channel",
            "severity"
        ]

        missing = []
        
        

        for field in required_fields:

            if not route.get(field):

                missing.append(field)

        if missing:

            return {
                "success": False,
                "type": "complaints",
                "requires_input": True,
                "missing": missing,
                "answer": (
                    "I need more complaint details "
                    "before I can predict citizen "
                    "satisfaction."
                )
            }

        result = predict_complaints(
            **route
        )

        if "error" in result:

            return {
                "success": False,
                "type": "complaints",
                "error": result["error"]
            }

        answer = self.format_model_response(
    result,
    "complaints"
)

        return {
            "success": True,
            "type": "complaints",
            "answer": answer,
            "data": result
        }

    # ========================================================
    # GENERAL QUERY
    # ========================================================

    def handle_general(self, query):

        answer = self.generate_response(
            query=query,
            context=""
        )

        return {
            "success": True,
            "type": "general",
            "answer": answer
        }

    # ========================================================
    # LLM RESPONSE
    # ========================================================

    def generate_response(
        self,
        query,
        context=""
    ):

        # ----------------------------------------------------
        # If no LLM configured
        # ----------------------------------------------------

        if self.llm is None:

            return (
                "I processed your request.\n\n"
                f"Result:\n{context}"
            )

        # ----------------------------------------------------
        # Prompt
        # ----------------------------------------------------

        prompt = f"""
You are a Smart City AI Assistant for Mumbai.

Answer the user's question using only
the information provided in the context.

Do not invent values.

User question:
{query}

Context:
{context}

Give a concise and useful answer.
"""

        response = self.llm.invoke(
            prompt
        )

        # Handle different LLM response formats

        if hasattr(
            response,
            "content"
        ):

            return response.content

        return str(response)
    
    def format_model_response(self, result, intent):
        """
        Convert model JSON/dictionary output into
        friendly, readable text.
        """

        if not result:
            return "I couldn't find any results for your request."

        # Handle error
        if isinstance(result, dict) and "error" in result:
            return f"Sorry, I couldn't complete the prediction. {result['error']}"

        # ========================================================
        # AQI
        # ========================================================

        if intent == "aqi":

            # Get AQI value from possible keys
            aqi = (
                result.get("prediction")
                or result.get("predicted_aqi")
                or result.get("aqi")
                or result.get("us_aqi")
            )

            date = result.get(
                "date",
                "the requested date"
            )

            if aqi is None:
                return "I couldn't determine the AQI prediction."

            aqi = float(aqi)

            if aqi <= 50:
                category = "Good"
                advice = "Air quality is expected to be good."

            elif aqi <= 100:
                category = "Satisfactory"
                advice = "Air quality should be acceptable for most people."

            elif aqi <= 200:
                category = "Moderate"
                advice = "Sensitive individuals may want to reduce prolonged outdoor activity."

            elif aqi <= 300:
                category = "Poor"
                advice = "Consider limiting prolonged outdoor activity."

            elif aqi <= 400:
                category = "Very Poor"
                advice = "Avoid prolonged outdoor activity when possible."

            else:
                category = "Severe"
                advice = "Avoid outdoor exposure as much as possible."

            return (
                f"🌫️ **AQI Prediction**\n\n"
                f"For **{date}**, the predicted AQI is "
                f"**{aqi:.0f}**, which falls in the "
                f"**{category}** category.\n\n"
                f"💡 {advice}"
            )

        # ========================================================
        # TRAFFIC
        # ========================================================

        if intent == "traffic":

            area = result.get("area")
            road = result.get("road_name")
            date = result.get("date")
            hour = result.get("hour")

            congestion = result.get(
                "congestion_level"
            )

            speed = result.get(
                "avg_speed"
            )

            vehicles = result.get(
                "vehicle_count"
            )

            response = "🚦 **Traffic Prediction**\n\n"

            if area:
                response += f"📍 Area: **{area}**\n"

            if road:
                response += f"🛣️ Road: **{road}**\n"

            if date:
                response += f"📅 Date: **{date}**\n"

            if hour is not None:
                response += f"🕐 Time: **{hour}:00**\n"

            response += "\n"

            if congestion is not None:

                congestion = float(congestion)

                if congestion < 30:
                    traffic_status = "Low"
                elif congestion < 60:
                    traffic_status = "Moderate"
                elif congestion < 80:
                    traffic_status = "High"
                else:
                    traffic_status = "Very High"

                response += (
                    f"🚦 Congestion: **{congestion:.1f}%** "
                    f"({traffic_status})\n"
                )

            if speed is not None:
                response += (
                    f"🚗 Average speed: **{float(speed):.1f} km/h**\n"
                )

            if vehicles is not None:
                response += (
                    f"🚙 Vehicles: **{float(vehicles):.0f}**\n"
                )

            return response

        # ========================================================
        # COMPLAINTS
        # ========================================================

        if intent == "complaints":

            satisfaction = (
                result.get("satisfaction")
                or result.get("satisfaction_score")
                or result.get("predicted_satisfaction")
            )

            if satisfaction is None:
                return (
                    "I couldn't determine the predicted "
                    "citizen satisfaction."
                )

            satisfaction = float(satisfaction)

            if satisfaction >= 80:
                status = "Very Satisfied"
            elif satisfaction >= 60:
                status = "Satisfied"
            elif satisfaction >= 40:
                status = "Neutral"
            elif satisfaction >= 20:
                status = "Dissatisfied"
            else:
                status = "Very Dissatisfied"

            return (
                "📢 **Citizen Satisfaction Prediction**\n\n"
                f"⭐ Predicted satisfaction: "
                f"**{satisfaction:.1f}%**\n\n"
                f"Overall status: **{status}**"
            )

        # ========================================================
        # FALLBACK
        # ========================================================

        return (
            "I found the following result:\n\n"
            f"{result}"
        )