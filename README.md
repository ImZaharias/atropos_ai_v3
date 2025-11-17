![Exam Page](https://github.com/ImZaharias/atropos_ai_v3/blob/main/atropos.png)


# 🧵 Atropos AI  
### Η σοφία που καθορίζει τον δρόμο σου  

---

## 📖 Περιγραφή

Το **Atropos AI** είναι ένα *έμπειρο σύστημα* (expert system) βασισμένο σε **κανόνες** και **Flask**.  
Μέσα από 11 ερωτήσεις, προβλέπει σε ποιον τομέα της Πληροφορικής ταιριάζει περισσότερο ο χρήστης  
(π.χ. Software, Cloud, AI, Salesforce, Support, Consulting κ.ά.).

Το όνομα “Atropos” προέρχεται από τη Μοίρα που “κόβει το νήμα” —  
εδώ όμως, η Ατρόπος καθοδηγεί τον δρόμο σου στην τεχνολογία.

---

## 🧠 Μέθοδος Τεχνητής Νοημοσύνης

Χρησιμοποιείται μια **rule-based knowledge system** λογική,  
όπου κάθε ερώτηση ενεργοποιεί *effects* που επηρεάζουν βαθμολογίες για κάθε ρόλο.

- Οι απαντήσεις αυξάνουν/μειώνουν πόντους για συγκεκριμένους ρόλους.  
- Τα **κίνητρα** (Money, Challenge, Stability, Impact, κ.ά.) δίνουν bonus σε αντίστοιχους ρόλους.  
- Το τελικό αποτέλεσμα προκύπτει από **σταθμισμένο συνδυασμό** (weighted reasoning).  
- Η ανάλυση του “νήματος” φαίνεται στο trace view με φιλικό UI.

---

## ⚙️ Τεχνολογίες

- **Python 3.11+**
- **Flask 3.x**
- **SQLite3**
- **Jinja2 Templates**
- **HTML/CSS (custom theme – Atropos style)**

---

## 🧩 Δομή Εφαρμογής

| Αρχείο / Φάκελος | Περιγραφή |
|------------------|------------|
| `app.py` | Κύρια εφαρμογή Flask και ροή ερωτήσεων |
| `rules.py` | Κανόνες, bonus λογική, περιγραφές ρόλων |
| `questions.json` | Ορισμός ερωτήσεων και επιδράσεων |
| `templates/` | HTML templates με Jinja2 |
| `static/` | CSS και εικόνες (logo, theme) |
| `data.db` | SQLite βάση για αποτελέσματα και feedback |

---

## 🚀 Οδηγίες Εκτέλεσης

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
python app.py
