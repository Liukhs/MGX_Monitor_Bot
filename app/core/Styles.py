MAIN_STYLE = """
QMainWindow{
    background-color: qlineargradient(
    x1:0, y1:0, x2:1, y2:1,
    stop: 0 #f8fafc,
    stop: 1 #f1f5f9
    );
}
#HeaderFrame{
    background-color: #ffffff;
    padding: 12px 10px;
    border: 1px solid #e2e8f0;
}
#MainTitle{
    color: #0f172a;
    font-size: 26px;
    font-weight: 800;
}
#SubTitle{
    color: #64748b;
}
QPushButton{
    background-color: #ffffff;
    color: #334155;
    border-radius: 10px;
    padding: 12px 10px; 
    font-weight: bold;
    border: 1px solid #e2e8f0;
    font-size: 15px;
}
#StartButton{
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
}
#StartButton:hover{
    background-color: qlineargradient(
    x1:0, y1:0, x2:1, y2:1,
    stop: 0 #16a34a,
    stop: 1 #15803d
    );
}
QPushButton:hover{
    background-color: #f8fafc;
}
#LogHeader{
    background-color: qlineargradient(
    x1:0, y1:0, x2:1, y2:1,
    stop: 0 #334155,
    stop: 1 #1e293b
    );
    color: #ffffff;
    border-top-left-radius: 10px; 
    border-top-right-radius: 10px;
    border: 1px solid #475569;  
}
#LogLabel{
    color: #ffffff;
    font-weight: bold;
    font-size: 15px;
}
#LogArea{
    background-color: #050507;
    border: 1px solid #2d2d35;
    border-top: none;
    border-bottom: none;
}
#LogArea QWidget{
    background-color: #050507;
}
#StatusFooter{
    background-color: #f8fafc;
    border-bottom-left-radius: 10px;
    border-bottom-right-radius: 10px;
    height: 35px;
    border: 1px solid #e2e8f0
}
#StatusFooter QLabel{
    color: #555;
    font-weight: bold;
    font-size: 11px;
}
QProgressBar{
    background-color: #2b2b2b;
    border-radius: 4px;
}
QProgressBar::chunk{
    background-color: #1f538d;
}
"""