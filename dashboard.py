
# IMPORT CONFIGURATIONS

import streamlit as st
from plotly.subplots import make_subplots
from streamlit_metrics import metric, metric_row
import plotly.express as px
import pandas as pd
import numpy as np

# DEFINITIONS

y_scale = 'En miles de US$'

# SIDEBAR

fin_stmt = {'Información financiera': ['Principales indicadores',
                                       'Últimas noticias y hechos de importancia',
                                       'Balance General', 'Estado de Resultados',
                                       'Flujo de efectivo']}

types_df = pd.DataFrame(fin_stmt)
clist = types_df['Información financiera'].unique()
sidebar_options = st.sidebar.selectbox('Seleccione la información a visualizar:', clist)

# LOAD SOME DATA

balance_sheet = pd.read_csv('balance_sheet_annual2.csv', delimiter = ';')

income_statement = pd.read_csv('income_statement.csv', delimiter = ';')

# RESUMEN DE INDICADORES

if sidebar_options == 'Principales indicadores':

    st.title('Principales indicadores de Petroperú')

    st.write('Acá se mostrará un pequeño comentario y principales indicadores de Petroperú y '
             'sobre el Proyecto de Modernización de la Refinería de Talara')

    # MAIN INDICATORS RELATED TO PETROPERÙ

    st.subheader('Indicadores de seguimiento de Petroperú')

    st.write('indicadores financieros de Petroperú')

    # MAIN INDICATORS RELATED TO PMRT

    st.subheader('Indicadores del Proyecto de Modernización de la Refinería de Talara')

    kpi_main1, kpi_main2 = st.columns(2)

    kpi_main1.metric("Avance físico de obra", "96.79%", "4.05% a/a")

    kpi_main2.metric("Avance programado", "99.37%", "6.27% a/a")

# ÚLTIMAS NOTICIAS Y HECHOS DE IMPORTANCIA

elif sidebar_options == 'Últimas noticias y hechos de importancia':

    st.title('Información relevante sobre Petroperú')

    st.write('Escribir lo último sobre Petroperú')

    st.metric(label="Avance físico de obra", value="96.8%", delta="4.1%")
    kpi_latest1, kpi_latest2 = st.columns(2)

    kpi_latest1.metric("Avance físico de obra", "96.79%", "4.05%")
    kpi_latest2.metric("Avance programado", "99.37%", "6.27%")

elif sidebar_options == 'Balance General':

    # GET BALANCE SHEET DATA

    balance_sheet = pd.read_csv('balance_sheet_annual2.csv', delimiter= ';')

    # OPTIONS TO VISUALIZE ASSETS

    balance_list = {'Resumen', 'Situación de los activos', 'Situación de los pasivos',
                    'Análisis de ratios financieros'}

    sidebar_balance = st.sidebar.selectbox('Seleccione una opción:', balance_list)

    # TITLE

    #st.title('Análisis del Balance General de Petroperú')

    #st.write('Introducir un comentario sobre el análisis horizontal, vertical y de los '
    #         'principales ratios de Petroperú')

    # SUMMARY

    if sidebar_balance == 'Resumen':

        # SUMMARY OF THE BALANCE SHEET

        latest_year = balance_sheet['year'].iloc[-1]

        st.title('Resumen del Balance General de Petroperú al ' + str(latest_year) + ' (en miles de US$)')

        balance_sheet_summary = pd.DataFrame({'año': balance_sheet['year'],
                                              'Activos': balance_sheet['TOTAL ACTIVO'],
                                              'Pasivos': balance_sheet['TOTAL PASIVO'],
                                              'Patrimonio': balance_sheet['TOTAL PATRIMONIO']
                                              })

        # KPI's

        latest_assets = balance_sheet['TOTAL ACTIVO'].iloc[-1]

        assets_t1 = balance_sheet['TOTAL ACTIVO'].iloc[-2]

        delta_assets = latest_assets / assets_t1 - 1

        delta_assets = '{:.2%}'.format(delta_assets)

        latest_liabilities = balance_sheet['TOTAL PASIVO'].iloc[-1]

        liabilities_t1 = balance_sheet['TOTAL PASIVO'].iloc[-2]

        delta_liabilities = latest_liabilities / liabilities_t1 - 1

        delta_liabilities = '{:.2%}'.format(delta_liabilities)

        latest_equity = balance_sheet['TOTAL PATRIMONIO'].iloc[-1]

        equity_t1 = balance_sheet['TOTAL PATRIMONIO'].iloc[-2]

        delta_equity = latest_equity / equity_t1 - 1

        delta_equity = '{:.2%}'.format(delta_equity)

        kpi_summary1, kpi_summary2, kpi_summary3 = st.columns(3)

        kpi_summary1.metric("Activos", f'{latest_assets:,}', delta_assets)

        kpi_summary2.metric("Pasivos", f'{latest_liabilities:,}', delta_liabilities, delta_color = 'inverse')

        kpi_summary3.metric("Patrimonio", f'{latest_equity:,}', delta_equity)

        # RESUMEN DE LOS ACTIVOS FINANCIEROS

        st.subheader('Resumen de los activos financieros')

        total_assets = pd.DataFrame({'año': balance_sheet['year'], 'Activos': balance_sheet['TOTAL ACTIVO']})

        fig_total_assets = px.bar(total_assets, x = 'año', y = 'Activos',
                                  labels = {'año': 'Año','Activos': y_scale}, text_auto = '.2s',
                                  title = 'Total de activos financieros')

        st.plotly_chart(fig_total_assets, use_container_width = True)

        # Composición de los activos financieros

        assets_summary = pd.DataFrame({'año': balance_sheet['year'],
                                     'Activo corriente': balance_sheet['Total activo corriente'],
                                     'Activo no corriente': balance_sheet['Total activo no corriente']})

        fig_assets = px.bar(assets_summary, x = 'año', y = ['Activo corriente', 'Activo no corriente']
                          , labels = {'año': 'Año'}, text_auto = '.2s')

        fig_assets.update_layout(yaxis_title = y_scale, title = 'Composición de los activos financieros',
                                 legend = dict(yanchor="top", y=0.99, xanchor="left", x=0.01))

        st.plotly_chart(fig_assets, use_container_width = True)

        # RESUMEN DE LOS PASIVOS FINANCIEROS

        st.subheader('Resumen de los pasivos financieros')

        total_liabilities = pd.DataFrame({'año': balance_sheet['year'],
                                          'Pasivos': balance_sheet['TOTAL PASIVO']})

        fig_total_liabilities = px.bar(total_liabilities, x = 'año', y = 'Pasivos',
                                  labels = {'año': 'Año','Pasivos': y_scale}, text_auto = '.2s',
                                  title = 'Total de pasivos financieros')

        st.plotly_chart(fig_total_liabilities, use_container_width = True)

        # Composición de los pasivos financieros

        liabilities_summary = pd.DataFrame({'año': balance_sheet['year'],
                                            'Pasivo corriente': balance_sheet['Total pasivo corriente'],
                                            'Pasivo no corriente': balance_sheet['Total pasivo no corriente']
                                            })

        fig_liabilities = px.bar(liabilities_summary, x = 'año', y = ['Pasivo corriente',
                                                                      'Pasivo no corriente'],
                                 labels = {'año': 'Año'}, text_auto = '.2s',
                                 title = 'Composición de los pasivos financieros')

        fig_liabilities.update_layout(yaxis_title = y_scale,
                                      legend = dict(yanchor="top", y=0.99, xanchor="left", x=0.01))

        st.plotly_chart(fig_liabilities, use_container_width = True)

        # SUMMARY OF EQUITY

        st.subheader('Resumen del patrimonio')

        total_equity = pd.DataFrame({'año': balance_sheet['year'],
                                          'Patrimonio': balance_sheet['TOTAL PATRIMONIO']})

        fig_total_equity = px.bar(total_equity, x = 'año', y = 'Patrimonio',
                                       labels = {'año': 'Año','Patrimonio': y_scale}, text_auto = '.2s',
                                       title = 'Total de patrimonio')

        st.plotly_chart(fig_total_equity, use_container_width = True)

    # ASSETS

    elif sidebar_balance == 'Situación de los activos':

        st.title('Situación de los activos financieros')

        st.subheader('Activo corriente')

        assets_cash = pd.DataFrame({'año': balance_sheet['year'],
                                    'Efectivo y equivalentes de efectivo':
            balance_sheet['Efectivo y equivalente de efectivo']})

        fig_cash = px.bar(assets_cash, x = 'año', y = 'Efectivo y equivalentes de efectivo',
                       labels = {'año': 'Año',
                                 'Efectivo y equivalentes de efectivo': 'Miles de US$'},
                          title='Efectivo y equivalentes de efectivo', text_auto = '.2s')

        st.plotly_chart(fig_cash, use_container_width=True)

    # LIABILITIES

    elif sidebar_balance == 'Situación de los pasivos':

        st.title('Situación de los pasivos financieros')

        st.text('Hola')

    elif sidebar_balance == 'Análisis de ratios financieros':

        st.title('Análisis de ratios financieros')

        # Ratios de liquidez

        st.header('I. Ratios de liquidez')

        # Ratio de liquidez

        st.subheader('1. Ratio de liquidez')

        assets_summary = pd.DataFrame({'año': balance_sheet['year'],
                                       'Activo corriente': balance_sheet['Total activo corriente'],
                                       'Activo no corriente': balance_sheet['Total activo no corriente']})

        liquidity_ratio = pd.DataFrame({'año': assets_summary['año'],
                                        'Ratio de liquidez': balance_sheet['Total activo corriente'] / balance_sheet['Total pasivo corriente']
                                        })

        fig_liquidity = px.bar(liquidity_ratio, x = 'año', y = 'Ratio de liquidez',
                          labels = {'año': 'Año', 'Ratio de liquidez': 'Número de veces'},
                               title='Ratio de liquidez', text_auto = '.2f')

        st.plotly_chart(fig_liquidity, use_container_width=True)

        st.latex(r'''Ratio\;de\;liquidez = \frac{Activo\;corriente}{Pasivo\;corriente}''')

        # Prueba ácida

        st.subheader ('2. Prueba ácida')

        prueba_acida = pd.DataFrame({'año': assets_summary['año'],
                                     'Prueba ácida': (balance_sheet['Total activo corriente'] -
                                                      balance_sheet['Inventarios']) /
                                                     balance_sheet['Total pasivo corriente']
        })

        fig_prueba_acida = px.bar(prueba_acida, x = 'año', y = 'Prueba ácida',
                               labels = {'año': 'Año', 'Prueba ácida': 'Número de veces'},
                               title='Prueba ácida', text_auto = '.2f')

        st.plotly_chart(fig_prueba_acida, use_container_width=True)

        st.latex(r'''Prueba\;ácida = \frac{(Activos\;corrientes - Inventarios)}{Pasivos\;corrientes}
        ''')

        # Prueba defensiva

        st.subheader('3. Prueba defensiva')

        prueba_defensiva = pd.DataFrame({'año': assets_summary['año'],
                                         'Prueba defensiva': balance_sheet['Efectivo y equivalente de efectivo'] /
                                                             balance_sheet['Total pasivo corriente']
                                         })

        fig_prueba_defensiva = px.bar(prueba_defensiva, x = 'año', y = 'Prueba defensiva',
                                  labels = {'año': 'Año', 'Prueba defensiva': 'Número de veces'},
                                  title='Prueba defensiva', text_auto = '.2%')

        st.plotly_chart(fig_prueba_defensiva, use_container_width=True)

        st.latex(r'''Prueba\;defensiva = \frac{Caja}{Pasivos\;corrientes}\%
        ''')

        # Capital de trabajo

        st.subheader('4. Capital de trabajo')

        capital_trabajo = pd.DataFrame({'año': assets_summary['año'],
                                        'Capital de trabajo': balance_sheet['Total activo corriente'] -
                                                            balance_sheet['Total pasivo corriente']
                                        })

        fig_capital_trabajo = px.bar(capital_trabajo, x = 'año', y = 'Capital de trabajo',
                                      labels = {'año': 'Año', 'Capital de trabajo': 'Número de veces'},
                                      title='Capital de trabajo', text_auto = '.2s')

        st.plotly_chart(fig_capital_trabajo, use_container_width=True)

        st.latex(r'''Capital\;de\;trabajo = Activo\;corriente - Pasivo\;corriente
        ''')

        # Ratios de eficiencia

        st.header('II. Ratios de eficiencia')

        # Rotación de cartera

        st.subheader('1. Rotación de cartera')

        rotacion_cartera = pd.DataFrame({'año': assets_summary['año'],
                                         'Rotación de cartera':
                                             (balance_sheet['Cuentas por cobrar comerciales'] +
                                              balance_sheet['Otras cuentas por cobrar'])
                                             * 360 / income_statement['Total ingresos']
        })

        fig_rotacion_cartera = px.bar(rotacion_cartera, x = 'año', y = 'Rotación de cartera',
                                     labels = {'año': 'Año', 'Rotación de cartera': 'Número de veces'},
                                     title='Rotación de cartera', text_auto = '.0f')

        st.plotly_chart(fig_rotacion_cartera, use_container_width = True)

        st.latex(r'''Rotación\;de\;cartera = \frac{Cuentas\;por\;cobrar * 360}{Ventas}
        ''')

        # Rotación de inventarios

        st.subheader('2. Rotación de inventarios')

        rotacion_inventarios = pd.DataFrame({'año': assets_summary['año'],
                                             'Rotación de inventarios': balance_sheet['Inventarios'] * 360 /
                                                                     income_statement['Costo de ventas'] * - 1
        })

        fig_rotacion_inventarios = px.bar(rotacion_inventarios, x = 'año', y = 'Rotación de inventarios',
                                      labels = {'año': 'Año', 'Rotación de inventarios': 'Número de veces'},
                                      title='Rotación de inventarios', text_auto = '.0f')

        st.plotly_chart(fig_rotacion_inventarios, use_container_width = True)

        st.latex(r'''Rotación\;de\;cartera = \frac{Inventarios * 360}{Costo\;de\;ventas}
        ''')

        # Rotación de caja

        st.subheader('3. Rotación de caja')

        rotacion_caja = pd.DataFrame({
            'año': assets_summary['año'], 'Rotación de caja': balance_sheet['Efectivo y equivalente de efectivo'] *
                                                              360 / income_statement['Total ingresos']
        })

        fig_rotacion_caja = px.bar(rotacion_caja, x = 'año', y = 'Rotación de caja',
                                          labels = {'año': 'Año', 'Rotación de caja': 'Número de veces'},
                                          title='Rotación de caja', text_auto = '.0f')

        st.plotly_chart(fig_rotacion_caja, use_container_width = True)

        st.latex(r'''Rotación\;de\;cartera = \frac{Inventarios * 360}{Costo\;de\;ventas}
        ''')

        # Rotación de activos

        st.subheader('4. Rotación de activos')

        rotacion_activos = pd.DataFrame({
            'año': assets_summary['año'], 'Rotación de activos': income_statement['Total ingresos'] /
                                                                 balance_sheet['TOTAL ACTIVO']
        })

        fig_rotacion_activos = px.bar(rotacion_activos, x = 'año', y = 'Rotación de activos',
                                   labels = {'año': 'Año', 'Rotación de activos': 'Número de veces'},
                                   title='Rotación de activos', text_auto = '.2f')

        st.plotly_chart(fig_rotacion_activos, use_container_width = True)

        st.latex(r'''Rotación\;de\;activos = \frac{Ventas}{Activos}
        ''')

        # Rotación de activo fijo

        st.subheader('5. Rotación de activo fijo')

        rotacion_act_fijo = pd.DataFrame({
            'año': assets_summary['año'],
            'Rotación de activo fijo': income_statement['Total ingresos'] /
                                   (balance_sheet['Propiedad, planta y equipo'] +
                                    balance_sheet['Propiedades de inversión'] +
                                    balance_sheet['Activos intangibles'] +
                                    balance_sheet['Activos por derecho de uso'])
        })

        fig_rotacion_act_fijo = px.bar(rotacion_act_fijo, x = 'año', y = 'Rotación de activo fijo',
                                      labels = {'año': 'Año', 'Rotación de activo fijo': 'Número de veces'},
                                      title='Rotación de activo fijo', text_auto = '.2f')

        st.plotly_chart(fig_rotacion_act_fijo, use_container_width = True)

        st.latex(r'''Rotación\;de\;activo\;fijo = \frac{Ventas}{Activo\;fijo}
        ''')

        # Ratios de solvencia

        st.header('III. Ratios de solvencia')

        # Ratio de endeudamiento

        st.subheader('1. Ratio de endeudamiento')

        ratio_endeudamiento = pd.DataFrame({
            'año': assets_summary['año'], 'Ratio de endeudamiento': balance_sheet['TOTAL PASIVO'] /
                                                                    balance_sheet['TOTAL PATRIMONIO']
        })

        fig_endeudamiento = px.bar(ratio_endeudamiento, x = 'año', y = 'Ratio de endeudamiento',
                                       labels = {'año': 'Año', 'Ratio de endeudamiento': 'Número de veces'},
                                       title='Ratio de endeudamiento', text_auto = '.2f')

        st.plotly_chart(fig_endeudamiento, use_container_width = True)

        st.latex(r'''Ratio\;de\;endeudamiento = \frac{Pasivo}{Patrimonio}
        ''')

        # Ratio de endeudamiento de corto plazo

        st.subheader('2. Ratio de endeudamiento de corto plazo')

        ratio_endeudamiento_cp = pd.DataFrame({
            'año': assets_summary['año'], 'Ratio de endeudamiento de corto plazo':
                balance_sheet['Total pasivo corriente'] / balance_sheet['TOTAL PATRIMONIO']
        })

        fig_endeudamiento_cp = px.bar(ratio_endeudamiento_cp, x = 'año',
                                      y = 'Ratio de endeudamiento de corto plazo',
                                   labels = {'año': 'Año', 'Ratio de endeudamiento de corto plazo':
                                       'Número de veces'}, title='Ratio de endeudamiento de corto plazo',
                                      text_auto = '.2f')

        st.plotly_chart(fig_endeudamiento_cp, use_container_width = True)

        st.latex(r'''Ratio\;de\;endeudamiento\;de\;corto\;plazo = \frac{Pasivo\;corriente}{Patrimonio}
        ''')

        # Ratio de endeudamiento de largo plazo

        st.subheader('3. Ratio de endeudamiento de largo plazo')

        ratio_endeudamiento_lp = pd.DataFrame({
            'año': assets_summary['año'], 'Ratio de endeudamiento de largo plazo':
                balance_sheet['Total pasivo no corriente'] / balance_sheet['TOTAL PATRIMONIO']
        })

        fig_endeudamiento_lp = px.bar(ratio_endeudamiento_lp, x = 'año',
                                      y = 'Ratio de endeudamiento de largo plazo',
                                      labels = {'año': 'Año', 'Ratio de endeudamiento de largo plazo':
                                          'Número de veces'}, title='Ratio de endeudamiento de largo plazo',
                                      text_auto = '.2f')

        st.plotly_chart(fig_endeudamiento_lp, use_container_width = True)

        st.latex(r'''Ratio\;de\;endeudamiento\;de\;largo\;plazo = \frac{Pasivo\;no\;corriente}{Patrimonio}
        ''')

        # Ratios de rentabilidad

        st.header('IV. Ratios de rentabilidad')

        # Total de ingresos

        st.subheader('Ingresos totales')

        ingresos_totales = pd.DataFrame({
            'año': assets_summary['año'], 'Ingresos totales': income_statement['Total ingresos'] / 1000
        })

        fig_ingresos_totales = px.bar(ingresos_totales, x = 'año', y = 'Ingresos totales',
                                      labels = {'año': 'Año', 'Ingresos totales': 'Ingresos totales'},
                                      title = 'Ingresos totales (en millones de US$)',
                                      text_auto = ',2f')

        st.plotly_chart(fig_ingresos_totales, use_container_width = True)

        # Margen bruto

        # Margen operativo

        # Margen neto

        # ROA

        # ROE

elif sidebar_options == 'Estado de Resultados':

    st.title('Análisis de los Estados Financieros de Petroperú')

    st.write('Introducir algún comentario sobre los Estados financieros de Petroperú')

elif sidebar_options == 'Flujo de efectivo':

    st.title('Análisis del flujo de efectivo de Petroperú')

    st.write('Introducir algún comentario sobre el Flujo de efectivo de Petroperú')

elif sidebar_options == 'Normas legales':

    st.title('Normas legales')

    st.write('Principales normas legales relacionadas a Petroperú y el PMRT.')