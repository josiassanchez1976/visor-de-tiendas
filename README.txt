INSTRUCCIONES DE USO LOCAL

1. Instalar dependencias:
   pip install -r requirements.txt

2. Ejecutar interfaz Streamlit:
   streamlit run app_refactor.py

3. Ejecutar API REST:
   uvicorn api_busqueda:app --reload

4. Probar API en:
   http://127.0.0.1:8000/docs

5. Ejecutar pruebas:
   pytest test_app.py
