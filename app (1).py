import streamlit as st

st.set_page_config(page_title="Calculator", layout="centered")

# Keep the button grid in rows, even on a phone screen
st.markdown(
    """
    <style>
    div[data-testid="stHorizontalBlock"] { flex-wrap: nowrap !important; gap: 0.5rem; }
    div[data-testid="stColumn"], div[data-testid="column"] { min-width: 0 !important; flex: 1 1 0 !important; }
    div.stButton > button { height: 4rem; font-size: 1.5rem; }
    .display { text-align: right; padding: 1rem; border-radius: 12px;
               background: rgba(128,128,128,0.15); margin-bottom: 1rem; }
    .display .small { font-size: 1rem; opacity: 0.6; min-height: 1.4rem; }
    .display .big { font-size: 2.6rem; font-weight: 600; overflow-x: auto; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Calculator memory (survives each rerun)
defaults = {"display": "0", "prev": None, "op": None, "fresh": True}
for k, v in defaults.items():
    st.session_state.setdefault(k, v)


def calculate(a, op, b):
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "×":
        return a * b
    if op == "÷":
        return None if b == 0 else a / b


def fmt(x):
    return "Error" if x is None else f"{x:.10g}"


def press(key):
    s = st.session_state
    if s.display == "Error":
        s.update(defaults)

    if key.isdigit():
        if s.fresh or s.display == "0":
            s.display = key
        else:
            s.display += key
        s.fresh = False

    elif key == ".":
        if s.fresh:
            s.display, s.fresh = "0.", False
        elif "." not in s.display:
            s.display += "."

    elif key in "+-×÷":
        if s.op and s.prev is not None and not s.fresh:
            result = calculate(s.prev, s.op, float(s.display))
            s.display = fmt(result)
            if result is None:
                s.prev, s.op = None, None
                return
            s.prev = result
        else:
            s.prev = float(s.display)
        s.op, s.fresh = key, True

    elif key == "=":
        if s.op and s.prev is not None:
            result = calculate(s.prev, s.op, float(s.display))
            s.display = fmt(result)
            s.prev, s.op, s.fresh = None, None, True

    elif key == "C":
        s.update(defaults)


s = st.session_state
history = f"{fmt(s.prev)} {s.op}" if s.op else ""
st.markdown(
    f'<div class="display"><div class="small">{history}</div>'
    f'<div class="big">{s.display}</div></div>',
    unsafe_allow_html=True,
)

rows = [
    ["7", "8", "9", "÷"],
    ["4", "5", "6", "×"],
    ["1", "2", "3", "-"],
    ["0", ".", "=", "+"],
]
for row in rows:
    cols = st.columns(4)
    for col, label in zip(cols, row):
        col.button(label, key=f"key_{label}", on_click=press, args=(label,),
                   use_container_width=True)

st.button("C", key="key_C", on_click=press, args=("C",),
          use_container_width=True, type="primary")
