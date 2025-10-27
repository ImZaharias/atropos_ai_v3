# rules.py — Atropos AI

ROLES = ["Software","Cloud","AI","Salesforce","Support","QA","Design","Consulting","Security","Architecture"]

def init_scores():
    return {k: 0 for k in ROLES}

TROLL_LINES = [
    "Το νήμα ξεκινά. Μην το μπερδέψεις με το καλώδιο παραγωγής.",
    "Οι Μοίρες κοιτούν. Εσύ απάντα χωρίς φόβο (και χωρίς deploy).",    "Μικρή δοκιμή σοφίας — όχι, το cloud δεν είναι ο καιρός.",
    "Το μονοπάτι χαράσσεται. Επέλεξε με σύνεση (ή τύχη).",    "Το ψαλίδι της Ατρόπου δοκιμάζει την αυτοπεποίθησή σου.",
    "Τα logs μιλούν. Άκουσέ τα πριν μιλήσεις στους θεούς.",
    "Η άγνοια είναι επιτρεπτή· το ψέμα όχι. Προχώρα.",
    "Η παραγωγή σε κρίνει, όχι εγώ. Συνέχισε.",
    "Δυο ερωτήσεις ακόμη και η μοίρα θα μιλήσει.",
    "Τελευταίο βήμα. Το νήμα δένει τον προορισμό."
]

def apply_effects(scores: dict, motivation: dict, effects: dict):
    for k, v in effects.items():
        if k == "motivation":
            for m, w in v.items():
                motivation[m] = motivation.get(m, 0) + w
        else:
            if k in scores:
                scores[k] += v

def finalize_result(scores: dict, motivation: dict):
    blend = 0.5
    bonus = {
        "Money": {"Consulting": 0.5, "Salesforce": 0.5, "Cloud": 0.3},
        "Stability": {"Support": 0.5, "QA": 0.4, "Salesforce": 0.3},
        "Challenge": {"AI": 0.6, "Architecture": 0.5, "Software": 0.4, "Security": 0.4},
        "Ease": {"Support": 0.2},
        "Prestige": {"Architecture": 0.5, "AI": 0.4, "Design": 0.4},
        "Impact": {"Security": 0.4, "Consulting": 0.3},
    }

    adj = scores.copy()
    for m, mv in motivation.items():
        for r, w in bonus.get(m, {}).items():
            if r in adj:
                adj[r] += mv * blend * w

    ordered = sorted(adj.items(), key=lambda x: x[1], reverse=True)
    top_role, _ = ordered[0]

    descriptions = {
        "Cloud": "Ασχολείσαι με υποδομές, pipelines, DevOps και αυτοματοποίηση περιβάλλοντος.",
        "Consulting": "Βοηθάς άλλους να λύσουν προβλήματα και συνδέεις την τεχνολογία με τον άνθρωπο.",
        "Support": "Κρατάς συστήματα & ανθρώπους ασφαλείς και λειτουργικούς, με έμφαση στην εξυπηρέτηση.",
        "Software": "Γράφεις, διορθώνεις και βελτιώνεις κώδικα — η λογική είναι το όπλο σου.",
        "AI": "Αναζητάς γνώση πίσω από τα δεδομένα και χτίζεις ευφυή συστήματα.",
        "Salesforce": "Χτίζεις αυτοματισμούς και συνδέεις επιχειρησιακά δεδομένα για καλύτερες αποφάσεις.",
        "QA": "Εξασφαλίζεις ότι τίποτα δεν σπάει — πριν το μάθει ο χρήστης.",
        "Architecture": "Σχεδιάζεις το πώς όλα συνδέονται· βλέπεις το μεγάλο πλάνο.",
        "Security": "Προστατεύεις δεδομένα και ανθρώπους· σκέφτεσαι πάντα ένα βήμα μπροστά.",
        "Design": "Δίνεις σχήμα, χρώμα και εμπειρία στα συστήματα· η αισθητική σε οδηγεί.",
    }

    top3 = ordered[:3]
    reasoning_lines = ["Κορυφαίες κατευθύνσεις:"]
    for r, sc in top3:
        reasoning_lines.append(f"- {r} ({sc:.1f}): {descriptions.get(r, '')}")

    reasoning = "\n".join(reasoning_lines)
    return top_role, reasoning, ordered
