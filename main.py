from flask import Flask, render_template, request
from math import factorial
import sympy as sp
import math

app = Flask(__name__)




@app.route('/')
def index():
    return render_template('tema1.html')

@app.route('/calcular', methods=['POST'])
def calcular():
    try:
        # Obtener datos del formulario
        funcion = request.form.get('funcion', '').strip()
        edad_str = request.form.get('edad', '').strip()

        # Validar entradas
        if not funcion or not edad_str:
            return render_template('tema1.html', error="Por favor ingrese la función y la edad.", funcion=funcion, edad=edad_str)

        # Permitir uso de ^ para potencias
        funcion = funcion.replace('^', '**')

        # Convertir edad a número (float)
        x_valor = float(edad_str)

        # Definir variable simbólica
        x = sp.Symbol('x')

        # Convertir la función a expresión simbólica de forma segura
        expr = sp.sympify(funcion)

        resultado_numerico = float(expr.subs(x, x_valor))

        # Código de error de sobrevivencia
        if abs(resultado_numerico) < 1e-9:
            return render_template('tema1.html', error="Coloque una funcion de sobrevivencia valida", funcion=funcion, edad=edad_str)

        # --- después de haber creado `expr` y calculado `resultado_numerico` ---
        # Generar representación LaTeX con SymPy para que MathJax lo renderice correctamente.

        # Paso 1: función simbólica (en LaTeX)
        try:
            func_latex = sp.latex(expr)  # convierte la expresión simbólica a LaTeX
        except Exception:
            # fallback: mostrar la cadena tal cual (reemplazando '**' por '^' para mejor lectura)
            func_latex = funcion.replace('**', '^')

        # Paso 2: evaluar la expresión simbólica con x = x_valor y obtener LaTeX
        try:
            evaluated_expr = expr.subs(x, x_valor)
            evaluated_latex = sp.latex(evaluated_expr)
        except Exception:
            evaluated_latex = str(expr.subs(x, x_valor))

        # Paso 3: valor numérico redondeado (mostramos como número, no como LaTeX complejo)
        numeric_rounded = round(resultado_numerico, 4)
        numeric_latex = str(numeric_rounded)

        # Construir lista de pasos en LaTeX
        paso1 = rf"\mathbf{{S(x)}} = {func_latex}"
        paso2 = rf"\mathbf{{S({x_valor})}} = {evaluated_latex}"
        

        pasos = [paso1, paso2]

        # Retornar render_template con pasos en LaTeX
        return render_template(
            'tema1.html',
            resultado=resultado_numerico,
            pasos=pasos,
            funcion=funcion,
            edad=x_valor
        )

    except Exception as e:
        return render_template('tema1.html', error=f"Error: {e}", funcion=request.form.get('funcion', ''), edad=request.form.get('edad', ''))



#Tema 2 
#Tema 2 
@app.route('/tema2')
def tema2():
    return render_template('tema2.html')


@app.route('/calcular2', methods=['POST'])
def calcular_tema2():
    try:
        funcion = request.form.get('funcion', '').strip()
        x_valor = request.form.get('x_valor', '').strip()

        if not funcion or not x_valor:
            return render_template('tema2.html', error="Por favor ingrese la función S(x) y el valor de x.", funcion=funcion, x_valor=x_valor)

        # Permitir potencias con ^
        funcion_safe = funcion.replace('^', '**')

        # Convertir x a número
        try:
            x_num = float(x_valor)
        except ValueError:
            return render_template('tema2.html', error="El valor de x debe ser un número válido.", funcion=funcion, x_valor=x_valor)

        x = sp.Symbol('x')

        # Crear expresión simbólica
        try:
            expr = sp.sympify(funcion_safe)
        except Exception:
            return render_template('tema2.html', error="La función ingresada no es válida. Verifica la sintaxis.", funcion=funcion, x_valor=x_valor)

        # Evaluación de S(x)
        Sx_sym = expr.subs(x, x_num)
        Sx_float = float(Sx_sym)

        # Cálculo de F(x)
        fx_float = 1.0 - Sx_float

        if abs(fx_float) < 1e-9:
            return render_template('tema2.html', error="Coloque una funcion de sobrevivencia valida", funcion=funcion, x_valor=x_valor)

        

        # Función simbólica
        try:
            func_latex = sp.latex(expr)
        except Exception:
            func_latex = funcion.replace('**', '^')

        # Evaluación de S(x)
        try:
            Sx_latex = sp.latex(Sx_sym)
        except:
            Sx_latex = str(Sx_sym)

        # F(x) = 1 - S(x)
        numeric_latex = str(round(fx_float, 6))
        S_numeric_latex = str(round(Sx_float, 6))

        # Pasos en LaTeX
        paso1 = rf"\mathbf{{F(x)}} = 1 - S(x)"
        paso2 = rf"\mathbf{{1 - S({x_num})}} = 1 - {func_latex}"
        paso4 = rf"\mathbf{{1 - S({x_num})}} = 1 - {S_numeric_latex}"
        paso5 = rf"\mathbf{{f(x)}} = {numeric_latex}"

        pasos = [paso1, paso2, paso4, paso5]

        return render_template(
            'tema2.html',
            resultado=fx_float,
            pasos=pasos,
            funcion=funcion,
            x_valor=x_num
        )

    except Exception as e:
        return render_template('tema2.html', error=f"Error inesperado: {e}", funcion=request.form.get('funcion', ''), x_valor=request.form.get('x_valor', ''))


    

# Tema 3
@app.route('/tema3')
def tema3():
    return render_template('tema3.html')


@app.route('/calcular3', methods=['POST'])
def calcular_tema3():
    try:
        funcion = request.form.get('funcion', '').strip()
        a_str = request.form.get('a', '').strip()
        b_str = request.form.get('b', '').strip()
        m_str = request.form.get('m', '').strip()

        if not funcion or not a_str or not b_str or not m_str:
            return render_template('tema3.html',
                                   error="Por favor ingrese la función y los valores a, b y m.",
                                   funcion=funcion, a=a_str, b=b_str, m=m_str)

        # Convertir números
        try:
            a = float(a_str)
            b = float(b_str)
            m = float(m_str)
        except ValueError:
            return render_template('tema3.html',
                                   error="Los valores deben ser numéricos.",
                                   funcion=funcion, a=a_str, b=b_str, m=m_str)

        # Función segura
        funcion_safe = funcion.replace("^", "**")

        x = sp.Symbol('x')

        # Crear expresión simbólica
        try:
            expr = sp.sympify(funcion_safe)
        except Exception:
            return render_template('tema3.html',
                                   error="La función ingresada no es válida.",
                                   funcion=funcion, a=a_str, b=b_str, m=m_str)

        # Evaluar S(a), S(b), S(m)
        Sa_sym = expr.subs(x, a)
        Sb_sym = expr.subs(x, b)
        Sm_sym = expr.subs(x, m)

        Sa = float(Sa_sym)
        Sb = float(Sb_sym)
        Sm = float(Sm_sym)

        if Sm == 0:
            return render_template('tema3.html',
                                   error="S(m) no puede ser cero.",
                                   funcion=funcion, a=a, b=b, m=m)

        resultado = (Sa - Sb) / Sm

        if abs(resultado) < 1e-9:
            return render_template('tema3.html',
                                   error="Coloque una función de sobrevivencia válida.",
                                   funcion=funcion, a=a, b=b, m=m)

       
        # Función en LaTeX
        try:
            func_latex = sp.latex(expr)
        except:
            func_latex = funcion.replace('**', '^')

        # Valores en LaTeX
        Sa_latex = sp.latex(Sa_sym)
        Sb_latex = sp.latex(Sb_sym)
        Sm_latex = sp.latex(Sm_sym)

        res_latex = str(round(resultado, 6))

        # ----------------- PASOS -----------------
        paso1 = rf"\mathbf{{P(a < X < b \mid X > m)}} = \frac{{S(a) - S(b)}}{{S(m)}}"
        paso2 = rf"\mathbf{{\frac{{S({a}) - S({b})}}{{S({m})}}}}"
        paso3 = rf"\mathbf{{\frac{{ {func_latex} \;|_{{x={a}}} \;-\; {func_latex} \;|_{{x={b}}} }}{{ {func_latex} \;|_{{x={m}}} }}}}"
        paso4 = rf"\mathbf{{\frac{{ {Sa_latex} - {Sb_latex} }}{{ {Sm_latex} }}}}"
        paso5 = rf"\mathbf{{ = {res_latex} }}"

        pasos = [paso1, paso2, paso3, paso4, paso5]

        return render_template('tema3.html',
                               resultado=resultado,
                               pasos=pasos,
                               Sa=Sa, Sb=Sb, Sm=Sm,
                               a=a, b=b, m=m,
                               funcion=funcion)

    except Exception as e:
        return render_template('tema3.html',
                               error=f"Error inesperado: {e}",
                               funcion=request.form.get('funcion', ''),
                               a=request.form.get('a', ''),
                               b=request.form.get('b', ''),
                               m=request.form.get('m', ''))


# -------------------------------
#  EJECUCIÓN DEL SERVIDOR
# -------------------------------
if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

