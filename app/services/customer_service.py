from app.services.data_loader import load_all_data

def get_consolidated_customers():
    data = load_all_data()
    
    customers = {}
    
    for loan in data["loans"]:
        cid = loan["customer_id"]
        customers.setdefault(cid, {"customer_id": cid, "loans": [], "cards": [], "payments": [], "credit_scores": [], "cashflow": {}, "eligible_offers": []})
        customers[cid]["loans"].append(loan)

    for card in data["cards"]:
        cid = card["customer_id"]
        customers.setdefault(cid, {"customer_id": cid, "loans": [], "cards": [], "payments": [], "credit_scores": [], "cashflow": {}, "eligible_offers": []})
        customers[cid]["cards"].append(card)

    for payment in data["payments"]:
        cid = payment["customer_id"]
        if cid in customers:
            customers[cid]["payments"].append(payment)

    for score in data["scores"]:
        cid = score["customer_id"]
        if cid in customers:
            customers[cid]["credit_scores"].append(score)

    for cashflow in data["cashflows"]:
        cid = cashflow["customer_id"]
        if cid in customers:
            customers[cid]["cashflow"] = cashflow

    for customer in customers.values():
        total_balance = 0
        all_current = True
        for loan in customer["loans"]:
            total_balance += float(loan["principal"])
            if int(loan["days_past_due"]) > 30:
                all_current = False
        for card in customer["cards"]:
            total_balance += float(card["balance"])
            if int(card["days_past_due"]) > 30:
                all_current = False

        score = next((int(s["credit_score"]) for s in sorted(customer["credit_scores"], key=lambda x: x["date"], reverse=True)), None)

        for offer in data["offers"]:
            if total_balance <= offer["max_consolidated_balance"]:
                eligible = False
                if offer["conditions"] == "No mora >30 días al momento de la solicitud":
                    if all_current:
                        eligible = True
                elif offer["conditions"] == "Score > 650 y sin mora activa":
                    if score and score > 650 and all_current:
                        eligible = True
                if eligible:
                    customer["eligible_offers"].append(offer)

    return list(customers.values())

def find_customer_by_id(customer_id: str):
    print(customer_id)
    customers = get_consolidated_customers()
    for customer in customers:
        if customer["customer_id"] == customer_id:
            return customer
    return None