# Generated from: CODE_COMPLETE_VERSION_1.ipynb
# Converted at: 2026-03-16T21:38:11.166Z
# Next step (optional): refactor into modules & generate tests with RunCell
# Quick start: pip install runcell

import pandas as pd
import unicodedata
import ipywidgets as widgets
from IPython.display import display, clear_output, HTML


!pip install ipywidgets

import ipywidgets as widgets
from IPython.display import display

test = widgets.IntSlider(description="Test")
display(test)

display(ui)
refresh_outputs()

# 1) PARAMÈTRES FICHIERS
# =========================================================

carbon_file = "carbon_data.html"
companies_file = "entreprises.xlsx"

# 2) PARAMÈTRES MÉTIER
# =========================================================

REPL_MAP = {
    r"\'ea": "ê",
    r"\'e9": "é",
    r"\'e8": "è",
    r"\'b": "",
    r"\'ef": "ï",
    r"\'e7": "ç",
    r"\'e2": "â",
    r"\'9c": "œ",
    r"\'e0": "à",
    r"\'ee": "î",
}

SELECTOR_MAP = {
    "Menuiseries extérieures": "Extérieure",
    "Menuiserie intérieure": "Intérieure",
    "Revêtements de sol": "Sol",
    "Revêtements murs et plafonds": "Murs et plafonds",
    "Charpente - Ossature": "Charpente - Ossature",
    "Maçonnerie - Gros œuvre": "Maçonnerie - Gros œuvre",
    "Plomberie": "Plomberie",
    "Electricité": "Electricité",
    "Chauffage - Ventilation - Climatisation": "Chauffage - Ventilation - Climatisation",
}
CATEGORY_MERGE_MAP = {
    "Revêtements de sol": "Revêtements intérieurs",
    "Revêtements murs et plafonds": "Revêtements intérieurs",
    "Menuiseries extérieures": "Menuiseries",
    "Menuiserie intérieure": "Menuiseries",
    "Charpente - Ossature": "Structure",
    "Maçonnerie - Gros œuvre": "Structure",
    "Plomberie": "Réseaux techniques",
    "Electricité": "Réseaux techniques",
    "Chauffage - Ventilation - Climatisation": "Réseaux techniques",
}

LOW_CARBON_KEYWORDS = [
    "bas carbone",
    "chaume",
    "végétalisée",
    "biosourcé",
    "biosourcée",
    "laine",
    "chanvre",
    "ouate de cellulose",
]

basket = []

# 3) FONCTIONS UTILITAIRES
# =========================================================

def normalize_text(value: str) -> str:
    if pd.isna(value):
        return ""
    text = str(value).lower().strip()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return text

NORMALIZED_LOW_CARBON_KEYWORDS = [normalize_text(x) for x in LOW_CARBON_KEYWORDS]

def is_low_carbon_option(row: pd.Series) -> bool:
    text = f"{row.get('Sous_categorie', '')} {row.get('Produit_process', '')}"
    text_norm = normalize_text(text)
    keyword_match = any(keyword in text_norm for keyword in NORMALIZED_LOW_CARBON_KEYWORDS)

    emissions = row.get("Emissions_CO2")
    emissions_rule = pd.notna(emissions) and float(emissions) <= 0

    return keyword_match or emissions_rule

def split_categories(value):
    if pd.isna(value):
        return []
    text = str(value).replace("|", ";").replace(",", ";")
    return [x.strip() for x in text.split(";") if x.strip()]

# 4) CHARGEMENT DES DONNÉES CARBONE
# =========================================================

def load_carbon_df(html_path: str) -> pd.DataFrame:
    tables = pd.read_html(html_path)
    if not tables:
        raise ValueError("Aucun tableau trouvé dans carbon_data.html")

    df = tables[0].copy()

    df.columns = [
        "Categorie",
        "Sous_categorie",
        "Produit_process",
        "Unite",
        "Type_prestation",
        "Prestation",
        "Emissions_CO2",
    ]

    df = df.iloc[1:].reset_index(drop=True)

    for col in df.columns:
        if df[col].dtype == object:
            s = df[col].astype(str)
            for pat, repl in REPL_MAP.items():
                s = s.str.replace(pat, repl, regex=False)
            df[col] = s

    df["Emissions_CO2"] = pd.to_numeric(df["Emissions_CO2"], errors="coerce")
    df["Categorie_old"] = df["Categorie"]
    df["Selector"] = df["Categorie"].map(SELECTOR_MAP)
    df["Categorie"] = df["Categorie"].replace(CATEGORY_MERGE_MAP)

    return df

carbon_df = load_carbon_df(carbon_file)

def filter_companies_by_category(selected_category):
    result = companies_df[
        companies_df["Categorie_outil_liste"].apply(lambda cats: selected_category in cats)
    ].copy()

    cols = [
        "Entreprise",
        "Description",
        "Specificites",
        "Type_solution",
        "Pays_couverture",
        "Siege",
        "Lien",
    ]
    cols = [c for c in cols if c in result.columns]

    return result[cols].reset_index(drop=True)

# 5) CHARGEMENT DES DONNÉES ENTREPRISES
# =========================================================

def load_companies_df(file_path: str) -> pd.DataFrame:
    if file_path.endswith(".xlsx") or file_path.endswith(".xls"):
        df = pd.read_excel(file_path)
    elif file_path.endswith(".csv"):
        df = pd.read_csv(file_path, encoding="utf-8")
    else:
        raise ValueError("Format non supporté pour le fichier entreprises.")

    df.columns = df.columns.astype(str).str.strip()

    print("Colonnes détectées dans le fichier entreprises :")
    print(df.columns.tolist())

    rename_map = {
        "Entreprise": "Entreprise",
        "Description": "Description",
        "Spécificités": "Specificites",
        "Services": "Specificites",
        "Type de solution": "Type_solution",
        "Type de solution : technique, pratique ou les deux ?": "Type_solution",
        "indication du volume d'émissions qu'ils permettent d'économiser": "Volume_emissions_evitees",
        "Catégorie d’outil associée": "Categorie_outil",
        "Catégorie d'outil associée": "Categorie_outil",
        "Catégorie": "Categorie_outil",
        "Pays de couverture": "Pays_couverture",
        "Région de couverture": "Pays_couverture",
        "Siège(s) social(s)": "Siege",
        "Région du/des siège(s) social(s)": "Region_siege",
        "Lien": "Lien",
        "Link": "Lien",
        "Commentaires": "Commentaires",
        "Category List": "Category_List",
        "Subcategory List": "Subcategory_List",
    }

    df = df.rename(columns=rename_map)

    required_basic = ["Entreprise", "Categorie_outil"]
    for col in required_basic:
        if col not in df.columns:
            raise ValueError(f"Colonne obligatoire absente dans le fichier entreprises : {col}")

    df["Categorie_outil_liste"] = df["Categorie_outil"].apply(split_categories)

    return df

companies_df = load_companies_df(companies_file)

# 6) FONCTIONS MÉTIER
# =========================================================

def build_candidates(filtered_df: pd.DataFrame) -> pd.DataFrame:
    candidates = (
        filtered_df[
            [
                "Categorie",
                "Categorie_old",
                "Selector",
                "Sous_categorie",
                "Produit_process",
                "Unite",
                "Type_prestation",
                "Prestation",
                "Emissions_CO2",
            ]
        ]
        .dropna(subset=["Produit_process", "Emissions_CO2"])
        .drop_duplicates()
        .copy()
    )

    if candidates.empty:
        return candidates

    candidates["Option_famille"] = candidates.apply(
        lambda row: "Option bas carbone" if is_low_carbon_option(row) else "Standard",
        axis=1,
    )

    candidates = candidates.sort_values(
        ["Option_famille", "Emissions_CO2", "Produit_process"],
        ascending=[True, True, True],
    ).reset_index(drop=True)

    return candidates

def make_option_table(option_df: pd.DataFrame) -> pd.DataFrame:
    if option_df.empty:
        return option_df

    table = option_df.copy()
    table["Émissions spécifiques (kg CO₂ / unité)"] = table["Emissions_CO2"].astype(float).round(2)

    table = table[
        ["Produit_process", "Unite", "Émissions spécifiques (kg CO₂ / unité)"]
    ].rename(
        columns={
            "Produit_process": "Produit / process",
            "Unite": "Unité",
        }
    )

    return table.reset_index(drop=True)

def filter_companies_by_category(selected_category):
    result = companies_df[
        companies_df["Categorie_outil_liste"].apply(lambda cats: selected_category in cats)
    ].copy()

    cols = [
        "Entreprise",
        "Description",
        "Specificites",
        "Type_solution",
        "Pays_couverture",
        "Siege",
        "Region_siege",
        "Lien",
    ]
    cols = [c for c in cols if c in result.columns]

    return result[cols].reset_index(drop=True)


# 7) BLOCS DE PRÉSENTATION
# =========================================================

title_html = widgets.HTML("""
<div style="
    background: linear-gradient(90deg, #1f4e79, #2f75b5);
    color: white;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 15px;
">
    <h2 style="margin:0;">Bienvenue dans cet outil d’aide au chiffrage sinistre bas carbone</h2>
    <p style="margin:10px 0 0 0; line-height:1.5;">
        Il vous permet de sélectionner une solution de réparation, de comparer une option standard
        avec une alternative bas carbone, d’estimer les émissions de CO₂ associées et d’identifier
        les entreprises liées à la catégorie sélectionnée.
    </p>
</div>
""")

guide_html = widgets.HTML("""
<div style="
    background:#f5f7fa;
    border:1px solid #d9e2f3;
    padding:15px;
    border-radius:10px;
    margin-bottom:15px;
    line-height:1.6;
">
    <b>Parcours utilisateur</b><br>
    L’outil est organisé en quatre étapes : sélection du poste sinistré, estimation des émissions et comparaison des solutions,
    identification des entreprises liées à la catégorie choisie, puis récapitulatif du chiffrage.
</div>
""")

section_1 = widgets.HTML("<h3 style='color:#1f4e79;'>Étape 1 — Sélection du poste sinistré</h3>")
section_2 = widgets.HTML("<h3 style='color:#1f4e79;'>Étape 2 — Estimation des émissions et comparaison des solutions</h3>")
section_3 = widgets.HTML("<h3 style='color:#1f4e79;'>Étape 3 — Entreprises liées à la catégorie sélectionnée</h3>")
section_4 = widgets.HTML("<h3 style='color:#1f4e79;'>Étape 4 — Récapitulatif du chiffrage</h3>")

step1_text = widgets.HTML("""
<div style="margin-bottom:10px; color:#444; line-height:1.6;">
    Dans cette première étape, vous définissez le poste sinistré à partir de la catégorie,
    du niveau de détail technique et de la prestation concernée. Cette sélection permet
    d’orienter l’outil vers les solutions les plus pertinentes.
</div>
""")

step2_text = widgets.HTML("""
<div style="margin-bottom:10px; color:#444; line-height:1.6;">
    Une fois la solution choisie, l’outil estime les émissions de CO₂ associées à la quantité renseignée.
    Il affiche d’abord les solutions standard, puis les alternatives bas carbone. Un comparateur d’impact
    met également en évidence le gain carbone potentiel et formule une recommandation.
</div>
""")

step3_text = widgets.HTML("""
<div style="margin-bottom:10px; color:#444; line-height:1.6;">
    Cette étape présente les entreprises liées à la catégorie sélectionnée. Elle permet
    d’identifier rapidement des acteurs pertinents, leurs spécificités, leur zone de couverture,
    leur siège social et leurs informations principales.
</div>
""")

step4_text = widgets.HTML("""
<div style="margin-bottom:10px; color:#444; line-height:1.6;">
    Le récapitulatif du chiffrage rassemble toutes les lignes ajoutées, les quantités sélectionnées,
    les émissions associées à chaque ligne et le total global estimé en CO₂.
</div>
""")

impact_text = widgets.HTML("""
<div style="margin-bottom:10px; color:#444; line-height:1.6;">
    Lorsque des solutions standard et bas carbone existent pour le même poste, l’outil compare automatiquement
    leurs impacts afin de visualiser le gain carbone potentiel et d’aider à la décision.
</div>
""")


# 8) WIDGETS
# =========================================================

cat_dropdown = widgets.Dropdown(description="Catégorie :", layout=widgets.Layout(width="520px"))
selector_dropdown = widgets.Dropdown(description="Sélecteur :", layout=widgets.Layout(width="520px"))
sous_cat_dropdown = widgets.Dropdown(description="Sous-catégorie :", layout=widgets.Layout(width="520px"))
type_prest_dropdown = widgets.Dropdown(description="Type de prestation :", layout=widgets.Layout(width="520px"))
prest_dropdown = widgets.Dropdown(description="Prestation :", layout=widgets.Layout(width="520px"))

family_radio = widgets.RadioButtons(
    description="Type d’option :",
    options=[],
    layout=widgets.Layout(width="520px")
)

product_dropdown = widgets.Dropdown(
    description="Produit / process :",
    layout=widgets.Layout(width="750px")
)

qty_input = widgets.FloatText(
    description="Quantité :",
    value=1.0,
    layout=widgets.Layout(width="300px")
)

add_button = widgets.Button(
    description="Ajouter au chiffrage",
    button_style="success",
    layout=widgets.Layout(width="220px")
)

remove_button = widgets.Button(
    description="Retirer dernière ligne",
    button_style="warning",
    layout=widgets.Layout(width="200px")
)

clear_button = widgets.Button(
    description="Vider le chiffrage",
    button_style="danger",
    layout=widgets.Layout(width="180px")
)

download_button = widgets.Button(
    description="Exporter CSV",
    button_style="info",
    layout=widgets.Layout(width="150px")
)

metrics_output = widgets.Output()
impact_output = widgets.Output()
options_output = widgets.Output()
basket_output = widgets.Output()
debug_output = widgets.Output()
download_output = widgets.Output()
companies_output = widgets.Output()


# 9) ÉTAT GLOBAL
# =========================================================

current_candidates = pd.DataFrame()
current_selected_row = None

# =========================================================
# 10) LOGIQUE INTERFACE
# =========================================================

def get_active_filtered_df():
    d1 = carbon_df[carbon_df["Categorie"] == cat_dropdown.value]

    if selector_dropdown.layout.display == "none":
        d2 = d1
    else:
        d2 = d1[d1["Selector"] == selector_dropdown.value]

    d3 = d2[d2["Sous_categorie"] == sous_cat_dropdown.value]
    d4 = d3[d3["Type_prestation"] == type_prest_dropdown.value]
    d5 = d4[d4["Prestation"] == prest_dropdown.value]

    return d5

def refresh_categories():
    categories = sorted(carbon_df["Categorie"].dropna().unique().tolist())
    cat_dropdown.options = categories
    if categories:
        cat_dropdown.value = categories[0]

def update_selector(*args):
    d1 = carbon_df[carbon_df["Categorie"] == cat_dropdown.value]
    selector_options = sorted([x for x in d1["Selector"].dropna().unique().tolist() if x != ""])

    if len(selector_options) == 0:
        selector_dropdown.options = [""]
        selector_dropdown.value = ""
        selector_dropdown.layout.display = "none"
    else:
        selector_dropdown.layout.display = ""
        selector_dropdown.options = selector_options
        selector_dropdown.value = selector_options[0]

    update_sous_cat()
    refresh_companies()

def update_sous_cat(*args):
    d1 = carbon_df[carbon_df["Categorie"] == cat_dropdown.value]

    if selector_dropdown.layout.display == "none":
        d2 = d1
    else:
        d2 = d1[d1["Selector"] == selector_dropdown.value]

    options = sorted(d2["Sous_categorie"].dropna().unique().tolist())
    sous_cat_dropdown.options = options
    if options:
        sous_cat_dropdown.value = options[0]

    update_type_prest()

def update_type_prest(*args):
    d1 = carbon_df[carbon_df["Categorie"] == cat_dropdown.value]

    if selector_dropdown.layout.display == "none":
        d2 = d1
    else:
        d2 = d1[d1["Selector"] == selector_dropdown.value]

    d3 = d2[d2["Sous_categorie"] == sous_cat_dropdown.value]

    options = sorted(d3["Type_prestation"].dropna().unique().tolist())
    type_prest_dropdown.options = options
    if options:
        type_prest_dropdown.value = options[0]

    update_prest()

def update_prest(*args):
    d1 = carbon_df[carbon_df["Categorie"] == cat_dropdown.value]

    if selector_dropdown.layout.display == "none":
        d2 = d1
    else:
        d2 = d1[d1["Selector"] == selector_dropdown.value]

    d3 = d2[d2["Sous_categorie"] == sous_cat_dropdown.value]
    d4 = d3[d3["Type_prestation"] == type_prest_dropdown.value]

    options = sorted(d4["Prestation"].dropna().unique().tolist())
    prest_dropdown.options = options

    if options:
        prest_dropdown.value = options[0]

    update_products()

def update_products(*args):
    global current_candidates, current_selected_row

    d5 = get_active_filtered_df()
    current_candidates = build_candidates(d5)

    standard_df = current_candidates[current_candidates["Option_famille"] == "Standard"].reset_index(drop=True)
    low_carbon_df = current_candidates[current_candidates["Option_famille"] == "Option bas carbone"].reset_index(drop=True)

    available_families = []
    if not standard_df.empty:
        available_families.append("Standard")
    if not low_carbon_df.empty:
        available_families.append("Option bas carbone")

    if not available_families:
        family_radio.options = []
        product_dropdown.options = []
        current_selected_row = None
        refresh_outputs()
        return

    family_radio.options = available_families
    family_radio.value = available_families[0]

    update_product_list()

def update_product_list(*args):
    global current_selected_row

    if current_candidates.empty or not family_radio.options:
        product_dropdown.options = []
        current_selected_row = None
        refresh_outputs()
        return

    active_df = current_candidates[
        current_candidates["Option_famille"] == family_radio.value
    ].reset_index(drop=True)

    options = []
    for i, row in active_df.iterrows():
        label = f"{row['Produit_process']} — {float(row['Emissions_CO2']):.2f} kg CO₂ / {row['Unite']}"
        options.append((label, i))

    product_dropdown.options = options

    if options:
        product_dropdown.value = options[0][1]
        current_selected_row = active_df.loc[product_dropdown.value]
    else:
        current_selected_row = None

    refresh_outputs()

def update_selected_row(*args):
    global current_selected_row

    if current_candidates.empty or product_dropdown.value is None:
        current_selected_row = None
        refresh_outputs()
        return

    active_df = current_candidates[
        current_candidates["Option_famille"] == family_radio.value
    ].reset_index(drop=True)

    if len(active_df) > 0 and product_dropdown.value in active_df.index:
        current_selected_row = active_df.loc[product_dropdown.value]
    else:
        current_selected_row = None

    refresh_outputs()



# 11) COMPARATEUR D’IMPACT
# =========================================================

def refresh_impact_comparison():
    with impact_output:
        clear_output()

        d5 = get_active_filtered_df()
        comparison_candidates = build_candidates(d5)

        if comparison_candidates.empty:
            print("Aucune donnée disponible pour la comparaison d’impact.")
            return

        standard_df = comparison_candidates[
            comparison_candidates["Option_famille"] == "Standard"
        ].sort_values("Emissions_CO2", ascending=True)

        low_carbon_df = comparison_candidates[
            comparison_candidates["Option_famille"] == "Option bas carbone"
        ].sort_values("Emissions_CO2", ascending=True)

        if standard_df.empty or low_carbon_df.empty:
            print("Comparaison d’impact indisponible : il faut au moins une solution standard et une solution bas carbone.")
            return

        standard_row = standard_df.iloc[0]
        low_carbon_row = low_carbon_df.iloc[0]

        qty = float(qty_input.value)

        standard_total = float(standard_row["Emissions_CO2"]) * qty
        low_carbon_total = float(low_carbon_row["Emissions_CO2"]) * qty

        gain_absolute = standard_total - low_carbon_total

        if standard_total > 0:
            reduction_pct = (gain_absolute / standard_total) * 100
        else:
            reduction_pct = 0.0

        if gain_absolute > 0:
            recommendation = "Privilégier l’alternative bas carbone."
            recommendation_color = "#2e7d32"
        elif gain_absolute < 0:
            recommendation = "La solution standard présente ici un impact carbone inférieur."
            recommendation_color = "#c62828"
        else:
            recommendation = "Les deux solutions présentent un impact équivalent selon les données disponibles."
            recommendation_color = "#7f6000"

        display(HTML(f"""
        <div style="
            border:1px solid #d9e2f3;
            border-radius:12px;
            padding:16px;
            background:#f9fcff;
            margin:10px 0 15px 0;
        ">
            <h4 style="margin-top:0; color:#1f4e79;">Comparateur d’impact</h4>

            <div style="display:flex; gap:18px; flex-wrap:wrap; margin-top:10px;">
                <div style="padding:12px; border:1px solid #ddd; border-radius:10px; background:white; min-width:220px;">
                    <b>Émissions standard</b><br>
                    {standard_total:.2f} kg CO₂
                </div>

                <div style="padding:12px; border:1px solid #ddd; border-radius:10px; background:white; min-width:220px;">
                    <b>Émissions bas carbone</b><br>
                    {low_carbon_total:.2f} kg CO₂
                </div>

                <div style="padding:12px; border:1px solid #ddd; border-radius:10px; background:white; min-width:220px;">
                    <b>Gain carbone absolu</b><br>
                    {gain_absolute:.2f} kg CO₂
                </div>

                <div style="padding:12px; border:1px solid #ddd; border-radius:10px; background:white; min-width:220px;">
                    <b>Réduction</b><br>
                    {reduction_pct:.1f} %
                </div>
            </div>

            <div style="
                margin-top:14px;
                padding:12px;
                border-left:5px solid {recommendation_color};
                background:#ffffff;
                border-radius:8px;
            ">
                <b>Recommandation :</b> <span style="color:{recommendation_color};">{recommendation}</span>
            </div>

            <div style="margin-top:14px; line-height:1.6;">
                <b>Référence standard :</b> {standard_row['Produit_process']}<br>
                <b>Alternative bas carbone :</b> {low_carbon_row['Produit_process']}
            </div>
        </div>
        """))



# 12) AFFICHAGES
# =========================================================

def refresh_outputs():
    with metrics_output:
        clear_output()

        if current_selected_row is not None:
            unit = str(current_selected_row["Unite"]) if pd.notna(current_selected_row["Unite"]) else ""
            emissions_per_unit = float(current_selected_row["Emissions_CO2"])
            emissions_total = emissions_per_unit * float(qty_input.value)

            display(HTML(f"""
<div style="display:flex; gap:20px; margin:10px 0 15px 0; flex-wrap:wrap;">

    <div style="
        padding:16px;
        border:1px solid #d9e2f3;
        border-radius:12px;
        background:#ffffff;
        color:#1f1f1f;
        min-width:260px;
        box-shadow:0 2px 6px rgba(0,0,0,0.08);
    ">
        <div style="font-size:15px; font-weight:600; color:#1f4e79; margin-bottom:8px;">
            Émissions spécifiques
        </div>
        <div style="font-size:16px;">
            {emissions_per_unit:.2f} kg CO₂ / {unit}
        </div>
    </div>

    <div style="
        padding:16px;
        border:1px solid #d9e2f3;
        border-radius:12px;
        background:#ffffff;
        color:#1f1f1f;
        min-width:260px;
        box-shadow:0 2px 6px rgba(0,0,0,0.08);
    ">
        <div style="font-size:15px; font-weight:600; color:#1f4e79; margin-bottom:8px;">
            Émissions totales
        </div>
        <div style="font-size:16px;">
            {emissions_total:.2f} kg CO₂
        </div>
    </div>

</div>
"""))

    with options_output:
        clear_output()

        if current_candidates.empty:
            print("Aucune option produit / process disponible pour les critères sélectionnés.")
            refresh_basket()
            refresh_companies()
            refresh_impact_comparison()
            return

        standard_df = current_candidates[
            current_candidates["Option_famille"] == "Standard"
            ].reset_index(drop=True)

        low_carbon_df = current_candidates[
            current_candidates["Option_famille"] == "Option bas carbone"
            ].reset_index(drop=True)

        display(HTML("<h4 style='color:#7f6000;'>Solutions standard</h4>"))
        if standard_df.empty:
            print("Aucune solution standard trouvée.")
        else:
            display(make_option_table(standard_df))

        display(HTML("<h4 style='color:#2f75b5; margin-top:15px;'>Solutions bas carbone</h4>"))
        if low_carbon_df.empty:
            print("Aucune solution bas carbone trouvée.")
        else:
            display(make_option_table(low_carbon_df))

    with debug_output:
        clear_output()

        if current_selected_row is not None:
            display(HTML("<b>Détail de la ligne sélectionnée</b>"))
            debug_df = pd.DataFrame([current_selected_row]).copy()

            if "Categorie_old" in debug_df.columns:
                debug_df["Categorie"] = debug_df["Categorie_old"]

            debug_df = debug_df.drop(columns=["Categorie_old"], errors="ignore")
            display(debug_df)

    refresh_basket()
    refresh_companies()
    refresh_impact_comparison()


def refresh_basket():
    with basket_output:
        clear_output()

        if not basket:
            print("Aucune ligne ajoutée pour le moment.")
            return

        basket_df = pd.DataFrame(basket)
        basket_display = basket_df.copy()

        basket_display["Quantite"] = basket_display["Quantite"].round(2)
        basket_display["Emissions_specifiques"] = basket_display["Emissions_specifiques"].round(2)
        basket_display["kg_CO2_total"] = basket_display["kg_CO2_total"].round(2)

        basket_display = basket_display.rename(
            columns={
                "Selector": "Sélecteur",
                "Sous_categorie": "Sous-catégorie",
                "Type_prestation": "Type de prestation",
                "Option_famille": "Type d’option",
                "Produit_process": "Produit / process",
                "Unite": "Unité",
                "Quantite": "Quantité",
                "Emissions_specifiques": "Émissions spécifiques (kg CO₂ / unité)",
                "kg_CO2_total": "kg CO₂ total",
            }
        )

        display_cols = [
            "Categorie",
            "Sélecteur",
            "Sous-catégorie",
            "Type de prestation",
            "Prestation",
            "Type d’option",
            "Produit / process",
            "Unité",
            "Quantité",
            "Émissions spécifiques (kg CO₂ / unité)",
            "kg CO₂ total",
        ]

        display(basket_display[display_cols])

        total = float(basket_df["kg_CO2_total"].sum())
        display(HTML(f"<b>Total global estimé :</b> {total:.2f} kg CO₂"))


def refresh_companies():
    with companies_output:
        clear_output()

        selected_category = cat_dropdown.value
        company_result = filter_companies_by_category(selected_category)

       display(HTML(f"""
<div style="
    margin-top:10px;
    padding:16px;
    border:1px solid #d9e2f3;
    border-radius:12px;
    background:#ffffff;
    color:#1f1f1f;
    line-height:1.7;
    box-shadow:0 2px 6px rgba(0,0,0,0.08);
">
    <div style="font-size:15px; font-weight:600; color:#1f4e79; margin-bottom:8px;">
        Informations de correspondance
    </div>
    <div><b>Catégorie sélectionnée :</b> {selected_category}</div>
    <div><b>Entreprises identifiées :</b> {len(company_result)}</div>
</div>
"""))

        if len(company_result) == 0:
            print("Aucune entreprise trouvée pour cette catégorie.")
        else:
            display(company_result)

# 13) ACTIONS
# =========================================================

def add_to_basket(b):
    if current_selected_row is None:
        return

    unit = str(current_selected_row["Unite"]) if pd.notna(current_selected_row["Unite"]) else ""
    emissions_per_unit = float(current_selected_row["Emissions_CO2"])
    emissions_total = emissions_per_unit * float(qty_input.value)

    basket.append(
        {
            "Categorie": str(current_selected_row["Categorie"]),
            "Categorie_old": str(current_selected_row["Categorie_old"]),
            "Selector": "" if selector_dropdown.layout.display == "none" else str(selector_dropdown.value),
            "Sous_categorie": str(current_selected_row["Sous_categorie"]),
            "Type_prestation": str(current_selected_row["Type_prestation"]),
            "Prestation": str(current_selected_row["Prestation"]),
            "Option_famille": str(family_radio.value),
            "Produit_process": str(current_selected_row["Produit_process"]),
            "Unite": unit,
            "Quantite": float(qty_input.value),
            "Emissions_specifiques": float(emissions_per_unit),
            "kg_CO2_total": float(emissions_total),
        }
    )

    refresh_basket()

def remove_last(b):
    if basket:
        basket.pop()
    refresh_basket()

def clear_basket_func(b):
    basket.clear()
    refresh_basket()

def export_csv(b):
    if not basket:
        with download_output:
            clear_output()
            print("Le chiffrage est vide.")
        return

    basket_df = pd.DataFrame(basket)
    basket_df.to_csv("chiffrage_sinistre.csv", index=False, encoding="utf-8-sig")

    with download_output:
        clear_output()
        print("Fichier exporté : chiffrage_sinistre.csv")



# 14) ÉVÉNEMENTS
# =========================================================

cat_dropdown.observe(update_selector, names="value")
selector_dropdown.observe(update_sous_cat, names="value")
sous_cat_dropdown.observe(update_type_prest, names="value")
type_prest_dropdown.observe(update_prest, names="value")
prest_dropdown.observe(update_products, names="value")
family_radio.observe(update_product_list, names="value")
product_dropdown.observe(update_selected_row, names="value")
qty_input.observe(lambda change: refresh_outputs(), names="value")

add_button.on_click(add_to_basket)
remove_button.on_click(remove_last)
clear_button.on_click(clear_basket_func)
download_button.on_click(export_csv)

# =========================================================
# 15) AFFICHAGE FINAL
# =========================================================

refresh_categories()

ui = widgets.VBox([
    title_html,
    guide_html,

    section_1,
    step1_text,
    cat_dropdown,
    selector_dropdown,
    sous_cat_dropdown,
    type_prest_dropdown,
    prest_dropdown,
    family_radio,
    product_dropdown,
    qty_input,

    widgets.HTML("<hr>"),
    section_2,
    step2_text,
    metrics_output,

    widgets.HTML("<div style='margin-top:10px;'><h4 style='color:#1f4e79;'>Comparateur d’impact</h4></div>"),
    impact_text,
    impact_output,

    widgets.HBox([add_button, remove_button, clear_button, download_button]),
    download_output,

    widgets.HTML("<div style='margin-top:10px;'><h4 style='color:#1f4e79;'>Comparaison des solutions disponibles</h4></div>"),
    options_output,

    widgets.HTML("<hr>"),
    section_3,
    step3_text,
    companies_output,

    widgets.HTML("<hr>"),
    section_4,
    step4_text,
    basket_output,

    widgets.HTML("<hr>"),
    widgets.Accordion(children=[debug_output], selected_index=None)
])

display(ui)

ui.children[-1].set_title(0, "Afficher le détail technique de la ligne sélectionnée")

refresh_outputs()