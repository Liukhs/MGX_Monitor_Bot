#border radius
BORDER_RADIUS_SMALL = "8px"
BORDER_RADIUS_MID = "10px"
BORDER_RADIUS_BIG = "12px"
BORDER_RADIUS_ROUND = "9999px"
#padding
PADDING_HEADER = "24px 20px"
PADDING_PULSANTE = "12px 10px"
PADDING_BADGE_STATI = "12px 4px"
PADDING_BADGE_PICCOLI = "10px 4px"
PADDING_TABLE_CELLS = "24px 16px"
PADDING_TABLE_HEADERS = "6px 8px"
PADDING_FOOTER = "24px 12px"
PADDING_CONSOLE = "24px"
PADDING_RIGHE_CONSOLE = "0px 6px"
PADDING_CONTAINER_PROGRESSBAR = "16px"
#gap
HEADER_GAP = "12px"
SECTIONS_GAP = "24px"
GAP_PULSANTI = "16px"



MAIN_STYLE = f"""
QMainWindow{{
    background-color: qlineargradient(
    x1:0, y1:0, x2:1, y2:1,
    stop: 0 #f8fafc,
    stop: 1 #f1f5f9
    );
}}
#HeaderFrame{{
    background-color: #ffffff;
    padding: 12px 10px;
    border: 1px solid #e2e8f0;
}}
#MainTitle{{
    color: #0f172a;
    font-size: 26px;
    font-weight: 800;
}}
#SubTitle{{
    color: #64748b;
}}
QPushButton{{
    background-color: #ffffff;
    color: #334155;
    border-radius: 10px;
    padding: 12px 10px; 
    font-weight: bold;
    border: 1px solid #e2e8f0;
    font-size: 15px;
}}
#StartButton{{
    background-color: qlineargradient(
    x1:0, y1:0, x2:1, y2:1,
    stop: 0 #10ce50,
    stop: 1 #06b041
    );
    color: #ffffff;
    border-radius: 10px;
    padding: 12px 10px; 
    font-weight: bold;
    border: 1px solid #059d3a;
    font-size: 15px;
}}
#StartButton:hover{{
    background-color: qlineargradient(
    x1:0, y1:0, x2:1, y2:1,
    stop: 0 #16a34a,
    stop: 1 #15803d
    );
}}
QPushButton:hover{{
    background-color: #f8fafc;
}}
#LogHeader{{
    background-color: qlineargradient(
    x1:0, y1:0, x2:1, y2:1,
    stop: 0 #334155,
    stop: 1 #1e293b
    );
    color: #ffffff;
    border-top-left-radius: 10px; 
    border-top-right-radius: 10px;
    border: 1px solid #475569;  
}}
#LogLabel{{
    color: #ffffff;
    font-weight: bold;
    font-size: 15px;
}}
#LogArea{{
    background-color: #050507;
    border: 1px solid #2d2d35;
    border-top: none;
    border-bottom: none;
}}
#LogArea QWidget{{
    background-color: #050507;
}}
#StatusFooter{{
    background-color: #f8fafc;
    border-bottom-left-radius: 10px;
    border-bottom-right-radius: 10px;
    height: 35px;
    border: 1px solid #e2e8f0
}}
#StatusFooter QLabel{{
    color: #555;
    font-weight: bold;
    font-size: 11px;
}}
QProgressBar{{
    background-color: #c7c7c5;
    border-radius: 4px;
}}
QProgressBar::chunk{{
    background-color: green;
    border-radius: 4px;
}}
QHeaderView::section{{
    background-color: #f8fafC;
    border-bottom: 1px solid #e2e8f0;
    border-top: 1px solid #e2e8f0;
    color: #334155;
    padding: {PADDING_TABLE_HEADERS};
    text-align: left;
}}
QTableWidget {{
    background-color: #f8fafc !important;
    border: none;
    gridline-color: transparent;
    font-family: 'Segoe UI', sans-serif;
}}
QHeaderView::section {{
    background-color: #f8fafc;
    padding: 10px;
    border: none;
    border-bottom: 2px solid #e2e8f0;
    color: #64748b;
    font-weight: bold;
    text-transform: uppercase;
    font-size: 11px;
}}
QTableWidget::item {{
    border-bottom: 1px solid #f1f5f9;
    padding: 10px;
    color: #1e293b;
}}
#ProgressLayout{{ 
    border-radius: {BORDER_RADIUS_MID};
    border: 1px solid #e2e8f0;
    background-color: #ffffff;
    margin: 10px;
}}
#ProgressLayout QLabel{{  
    color: #000000;
    font-weight: bold;
    font-size: 12px;
}}
"""