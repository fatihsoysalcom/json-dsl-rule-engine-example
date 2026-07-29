import json

# --- JSON DSL Definition ---
# This JSON represents a Domain-Specific Language (DSL) for defining business rules.
# Each rule has conditions and actions. The article discusses whether defining rules
# this way truly eliminates "code" or merely shifts it to an interpreter.
BUSINESS_RULES_DSL = """
[
  {
    "name": "High Value Order Discount",
    "description": "Applies a 10% discount for orders over $100.",
    "conditions": [
      {
        "field": "total_amount",
        "operator": ">",
        "value": 100
      }
    ],
    "actions": [
      {
        "type": "set_discount_percentage",
        "value": 10
      }
    ]
  },
  {
    "name": "Loyalty Member Free Shipping",
    "description": "Provides free shipping for loyalty members with orders over $50.",
    "conditions": [
      {
        "field": "is_loyalty_member",
        "operator": "==",
        "value": true
      },
      {
        "field": "total_amount",
        "operator": ">=",
        "value": 50
      }
    ],
    "actions": [
      {
        "type": "set_shipping_cost",
        "value": 0
      }
    ]
  },
  {
    "name": "Small Order Surcharge",
    "description": "Adds a $5 surcharge for orders under $20.",
    "conditions": [
      {
        "field": "total_amount",
        "operator": "<",
        "value": 20
      }
    ],
    "actions": [
      {
        "type": "add_surcharge",
        "value": 5
      }
    ]
  }
]
"""

class RuleEngine:
    def __init__(self, rules_json_string):
        self.rules = json.loads(rules_json_string)
        # This __init__ method, and the entire class, is the "code"
        # that interprets the "no-code" JSON DSL. Without this Python code,
        # the JSON rules are just inert data.

    def _evaluate_condition(self, data, condition):
        field = condition["field"]
        operator = condition["operator"]
        value = condition["value"]

        # Access the field from the input data
        data_value = data.get(field)

        # This is where the "code" performs the actual logic defined in JSON.
        # Each operator needs explicit implementation in the underlying code.
        if operator == "==":
            return data_value == value
        elif operator == "!=":
            return data_value != value
        elif operator == ">":
            return data_value is not None and data_value > value
        elif operator == "<":
            return data_value is not None and data_value < value
        elif operator == ">=":
            return data_value is not None and data_value >= value
        elif operator == "<=":
            return data_value is not None and data_value <= value
        else:
            print(f"Warning: Unknown operator '{operator}'")
            return False

    def _execute_action(self, data, action):
        action_type = action["type"]
        action_value = action["value"]

        # This is the "code" that performs the actions specified in the JSON DSL.
        # Each action type requires a specific code implementation.
        if action_type == "set_discount_percentage":
            data["discount_percentage"] = action_value
            print(f"  Action: Set discount to {action_value}%")
        elif action_type == "set_shipping_cost":
            data["shipping_cost"] = action_value
            print(f"  Action: Set shipping cost to {action_value}")
        elif action_type == "add_surcharge":
            data["surcharge"] = data.get("surcharge", 0) + action_value
            print(f"  Action: Added surcharge of {action_value}")
        else:
            print(f"Warning: Unknown action type '{action_type}'")

    def process(self, input_data):
        # Create a mutable copy of the input data to apply changes
        processed_data = input_data.copy()
        processed_data.setdefault("discount_percentage", 0)
        processed_data.setdefault("shipping_cost", 5) # Default shipping cost
        processed_data.setdefault("surcharge", 0)

        print(f"\nProcessing order: {input_data}")
        print("Applying rules...")

        for rule in self.rules:
            all_conditions_met = True
            for condition in rule["conditions"]:
                if not self._evaluate_condition(processed_data, condition):
                    all_conditions_met = False
                    break # If any condition fails, this rule does not apply
            
            if all_conditions_met:
                print(f"Rule '{rule['name']}' triggered!")
                for action in rule["actions"]:
                    self._execute_action(processed_data, action)
            else:
                print(f"Rule '{rule['name']}' not met.")
        
        # Calculate final total based on applied rules
        final_total = processed_data["total_amount"]
        final_total -= (final_total * processed_data["discount_percentage"] / 100)
        final_total += processed_data["shipping_cost"]
        final_total += processed_data["surcharge"]
        processed_data["final_total"] = round(final_total, 2)

        print(f"Finished processing. Result: {processed_data}")
        return processed_data

# --- Example Usage ---
if __name__ == "__main__":
    # Initialize the rule engine with the JSON DSL
    engine = RuleEngine(BUSINESS_RULES_DSL)

    # Test cases representing different orders
    orders = [
        {"order_id": "ORD001", "total_amount": 120, "is_loyalty_member": False}, # High value discount
        {"order_id": "ORD002", "total_amount": 60, "is_loyalty_member": True},  # Loyalty free shipping
        {"order_id": "ORD003", "total_amount": 15, "is_loyalty_member": False}, # Small order surcharge
        {"order_id": "ORD004", "total_amount": 250, "is_loyalty_member": True}, # Both discount and free shipping
        {"order_id": "ORD005", "total_amount": 80, "is_loyalty_member": False}  # No rules apply
    ]

    for order in orders:
        engine.process(order)
