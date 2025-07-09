
# 🧭 Stakeholder 360

An interactive **Streamlit application** that visualizes organizational hierarchy from Excel data using `streamlit-agraph`. Built for **leadership teams** to easily explore stakeholders, view their managers, direct reports, and detailed context in a beautifully structured UI.

---

## 🚀 Features

- 📁 **Upload Excel** with stakeholder and manager hierarchy
- 🔽 **Select any stakeholder** from dropdown
- 📈 **Auto-generates org chart** (2nd degree → 1st degree → selected stakeholder → reportees)
- 🟩 Nodes show both **name and title** (`Name\nDesignation`)
- 🟦 Color-coded node roles:
  - Light Gray – 2nd Degree Manager
  - Blue – 1st Degree Manager
  - Green – Selected Stakeholder
  - Yellow – Direct Reportees
- 🖱️ **Hover to highlight** any node
- 🖼️ Clickable **LinkedIn profile** shown as person's name
- 📋 Beautifully styled tables for stakeholder details

---

## 📊 Example Org Chart Layout

```
  [2nd Degree Manager]
           ↓
   [1st Degree Manager]
           ↓
    [Selected Stakeholder]
           ↓
 [Reportee 1] [Reportee 2]
```

---

## 📝 Input Excel Format (required columns)

Your Excel file should include columns such as:

- `Client Name`
- `Designation`
- `1st degree Manager`
- `2nd Degree Manager`
- `Email address`
- `LinkedIn URL`
- `Location (from teams)`
- `Vendor CompanyName`
- ...and other optional fields used for detailed display.

---

## 🖥️ How to Run the App

### 🔧 1. Clone the repo

```bash
git clone https://github.com/your-org/stakeholder-org-chart
cd stakeholder-org-chart
```

### 🧱 2. Install dependencies

```bash
pip install -r requirements.txt
```

Make sure you have Python 3.8 or above.

### ▶️ 3. Run the Streamlit app

```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
├── app.py              # Main Streamlit app
├── utils.py            # Helper functions (optional)
├── data/               # Sample or uploaded Excel files
├── requirements.txt    # Python dependencies
└── README.md           # You are here!
```

---

## 📸 Screenshots

| Org Chart Example | Detail View Example |
|------------------|---------------------|
| ![Org Chart](./screenshots/org_chart.png) | ![Details](./screenshots/detail_view.png) |

---

## 🙌 Credits

- Built with [Streamlit](https://streamlit.io/)
- Visualization powered by [`streamlit-agraph`](https://github.com/ChrisDelClea/streamlit-agraph)

---

## 💼 Ideal Use Cases

- Leadership stakeholder visibility
- Account planning for B2B sales
- Organizational intelligence tools
- HR and org structure presentations

---

> Made with ❤️ by the Data Engineering & Insights Team
