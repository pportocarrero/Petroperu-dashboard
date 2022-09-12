
# IMPORT CONFIGURATIONS
import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

# LOAD SOME DATA

balance_sheet = pd.read_csv('balance_sheet_annual2.csv', delimiter=';')

income_statement = pd.read_csv('income_statement.csv', delimiter=';')

cash_flow = pd.read_csv('cash flow statement.csv', delimiter=';')

# AVANCE DEL PMRT

avance_pmrt_actual = 96.79  # CAMBIAR AVANCE ACTUAL DEL PMRT

avance_pmrt_anterior = 92.74  # CAMBIAR AVANCE ANTERIOR DEL PMRT

delta_avance_pmrt = (avance_pmrt_actual - avance_pmrt_anterior) * 100

avance_pmrt_prog_actual = 99.37  # CAMBIAR AVANCE ACTUAL PROGRAMADO DEL PMRT

avance_pmrt_prog_anterior = 93.10  # CAMBIAR AVANCE ANTERIOR PROGRAMADO DEL PMRT

delta_pmrt_prog = (avance_pmrt_prog_actual - avance_pmrt_prog_anterior) * 100

year_latest = 2021

# MONEDA DE TRABAJO

moneda = 'US$'

unidades = 'En millones de '

unidades_corto = 'MM '

empresa = 'Petroperú'

# SIDEBAR

fin_stmt = {'Información financiera': ['Principales indicadores',
                                       'Últimas noticias y hechos de importancia',
                                       'Balance General', 'Estado de Resultados']}

types_df = pd.DataFrame(fin_stmt)

clist = types_df['Información financiera'].unique()

sidebar_options = st.sidebar.selectbox('Seleccione la información a visualizar:', clist)

# RESUMEN DE INDICADORES

if sidebar_options == 'Principales indicadores':

    st.title('Principales indicadores de Petroperú (al ' + str(year_latest) + ')')

    st.write('Este tablero de control permite mostrar información relevante sobre Petroperú,'
             ' relacionada a sus resultados financieros y al Proyecto de Modernización de la Refineriía de'
             ' Talara.')

    # MAIN INDICATORS RELATED TO PETROPERÙ

    st.subheader('Indicadores de seguimiento de Petroperú')

    # KPI's DE COVENANTS

    # Deuda neta sobre patrimonio

    net_debt_equity = pd.DataFrame({
        'año': balance_sheet['year'],
        'Deuda neta sobre patrimonio': (
                (balance_sheet['Otros pasivos financieros no corrientes'] +
                 balance_sheet['Otros pasivos financieros'] -
                 balance_sheet['Efectivo y equivalente de efectivo']) /
                balance_sheet['TOTAL PATRIMONIO']
        )
                                          })

    net_debt_equity_latest = net_debt_equity['Deuda neta sobre patrimonio'].iloc[-1]

    year_latest = net_debt_equity['año'].iloc[-1]

    net_debt_equity_t1 = net_debt_equity['Deuda neta sobre patrimonio'].iloc[-2]

    year_t1 = net_debt_equity['año'].iloc[-2]

    delta_net_debt_equity = net_debt_equity_latest - net_debt_equity_t1

    # Cobertura de servicio de la deuda

    debt_srvc_cov = pd.DataFrame({
        'año': cash_flow['year'],
        'Cobertura del servicio de la deuda': (
                (cash_flow['Efectivo neto provisto por actividades de operación'] +
                 cash_flow['Pago de impuesto a las ganancias']) /
                (cash_flow['Pago de intereses'] * - 1)
        )
    })

    debt_srvc_cov_latest = debt_srvc_cov['Cobertura del servicio de la deuda'].iloc[-1]

    debt_srvc_cov_t1 = debt_srvc_cov['Cobertura del servicio de la deuda'].iloc[-2]

    delta_debt_srvc_cov = debt_srvc_cov_latest - debt_srvc_cov_t1

    # Deuda por PMRT

    pmrt = pd.DataFrame({
        'año': balance_sheet['year'],
        'Deuda por PMRT': balance_sheet['Otros pasivos financieros no corrientes'] / 1000
    })

    pmrt_latest = pmrt['Deuda por PMRT'].iloc[-1]

    pmrt_t1 = pmrt['Deuda por PMRT'].iloc[-2]

    delta_pmrt = pmrt_latest - pmrt_t1

    # KPIs DE COVENANTS

    kpi_convenants1, kpi_covenants2 = st.columns(2)

    kpi_convenants1.metric(
        'Deuda neta sobre patrimonio',
        f'{net_debt_equity_latest:,.2f}',
        f'{delta_net_debt_equity:,.2f}' + ' a/a',
        delta_color='inverse'
    )

    kpi_covenants2.metric(
        'Cobertura de servicio de la deuda',
        f'{debt_srvc_cov_latest:,.2f}',
        f'{delta_debt_srvc_cov:,.2f}' + ' a/a'
    )

    # kpi_covenants3.metric('Deuda del PMRT', f'{pmrt_latest:,.2f}',
    #                      f'{delta_pmrt:,.2f}' + ' (' + unidades_corto + moneda + ' a/a)', delta_color = 'inverse')

    # Gráficos de los ratios de los covenants

    # MAIN INDICATORS RELATED TO PMRT

    st.subheader('Indicadores del Proyecto de Modernización de la Refinería de Talara')

    # kpi_main1, kpi_main2 = st.columns(2)

    # kpi_main1.metric('Avance físico de obra', f'{avance_pmrt_actual:,.2%}', f'{delta_avance_pmrt:,.2f}' + ' p.p. a/a')

    # kpi_main2.metric('Avance programado', f'{avance_pmrt_prog_actual:,.2%}', f'{delta_pmrt_prog:,.2f}' + ' p.p. a/a')

    fig_pmrt = go.Figure()

    fig_pmrt.add_trace(go.Indicator(
        value=avance_pmrt_actual,
        delta={'reference': avance_pmrt_anterior},
        title={'text': 'Avance físico del PMRT (%)'},
        gauge={'axis': {'range': [None, 100]},
               'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 100}},
        domain={'row': 1, 'column': 0}))

    fig_pmrt.add_trace(go.Indicator(
        value=avance_pmrt_prog_actual,
        delta={'reference': avance_pmrt_prog_anterior},
        title={'text': 'Avance programado del PMRT (%)'},
        gauge={'axis': {'range': [None, 100]},
               'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 100}},
        domain={'row': 1, 'column': 1}))

    fig_pmrt.update_layout(
        grid={'rows': 1, 'columns': 2, 'pattern': "independent"},
        template={'data': {'indicator': [{
            'title': {'text': "Speed"},
            'mode': "number+delta+gauge",
        }]
        }})

    st.plotly_chart(fig_pmrt, use_container_width=True, height=1200, width=1000)

# ÚLTIMAS NOTICIAS Y HECHOS DE IMPORTANCIA

elif sidebar_options == 'Últimas noticias y hechos de importancia':

    st.title('Información relevante sobre Petroperú')

    st.write('Escribir lo último sobre Petroperú')

# BALANCE GENERAL

elif sidebar_options == 'Balance General':

    # GET BALANCE SHEET DATA

    balance_sheet = pd.read_csv('balance_sheet_annual2.csv', delimiter=';')

    # OPTIONS TO VISUALIZE ASSETS

    menu_opciones = {
        'Menú de opciones':
            ['Resumen',
             'Situación de los activos',
             'Situación de los pasivos',
             'Situación del patrimonio',
             'Análisis de ratios financieros']
                     }

    menu_df = pd.DataFrame(menu_opciones)

    menu_list = menu_df['Menú de opciones'].unique()

    sidebar_balance = st.sidebar.selectbox('Seleccione una opción:', menu_list)

    # RESUMEN

    if sidebar_balance == 'Resumen':

        # SUMMARY OF THE BALANCE SHEET

        latest_year = balance_sheet['year'].iloc[-1]

        st.title('Resumen del Balance General de Petroperú al ' + str(latest_year))

        balance_sheet_summary = pd.DataFrame({'año': balance_sheet['year'],
                                              'Activos': balance_sheet['TOTAL ACTIVO'],
                                              'Pasivos': balance_sheet['TOTAL PASIVO'],
                                              'Patrimonio': balance_sheet['TOTAL PATRIMONIO']
                                              })

        # KPI's

        latest_assets = balance_sheet['TOTAL ACTIVO'].iloc[-1] / 1000

        assets_t1 = balance_sheet['TOTAL ACTIVO'].iloc[-2] / 1000

        delta_assets = latest_assets / assets_t1 - 1

        delta_assets = '{:.1%}'.format(delta_assets)

        latest_liabilities = balance_sheet['TOTAL PASIVO'].iloc[-1] / 1000

        liabilities_t1 = balance_sheet['TOTAL PASIVO'].iloc[-2] / 1000

        delta_liabilities = latest_liabilities / liabilities_t1 - 1

        delta_liabilities = '{:.1%}'.format(delta_liabilities)

        latest_equity = balance_sheet['TOTAL PATRIMONIO'].iloc[-1] / 1000

        equity_t1 = balance_sheet['TOTAL PATRIMONIO'].iloc[-2] / 1000

        delta_equity = latest_equity / equity_t1 - 1

        delta_equity = '{:.1%}'.format(delta_equity)

        roa_latest = income_statement['Total resultados integrales'].iloc[-1] / balance_sheet['TOTAL ACTIVO'].iloc[-1]

        roa_t1 = income_statement['Total resultados integrales'].iloc[-2] / balance_sheet['TOTAL ACTIVO'].iloc[-2]

        delta_roa = (roa_latest - roa_t1) * 100

        delta_roa = '{:.1f}'.format(delta_roa)

        roe_latest = income_statement['Total resultados integrales'].iloc[-1] / balance_sheet['TOTAL PATRIMONIO'].iloc[-1]

        roe_t1 = income_statement['Total resultados integrales'].iloc[-2] / balance_sheet['TOTAL PATRIMONIO'].iloc[-2]

        delta_roe = (roe_latest - roe_t1) * 100

        delta_roe = '{:.1f}'.format(delta_roe)

        kpi_summary1, kpi_summary2, kpi_summary3, kpi_summary4, kpi_summary5 = st.columns(5)

        kpi_summary1.metric('Activos ' + '(' + unidades_corto + moneda + ')', f'{latest_assets:,.0f}', delta_assets)

        kpi_summary2.metric('Pasivos ' + '(' + unidades_corto + moneda + ')', f'{latest_liabilities:,.0f}', delta_liabilities, delta_color='inverse')

        kpi_summary3.metric('Patrimonio ' + '(' + unidades_corto + moneda + ')', f'{latest_equity:,.0f}', delta_equity)

        kpi_summary4.metric("ROA", f'{roa_latest:,.1%}', delta_roa + ' p.p.')

        kpi_summary5.metric("ROE", f'{roe_latest:,.1%}', delta_roe + ' p.p.')

        # RESUMEN DE LOS ACTIVOS FINANCIEROS

        st.subheader('Resumen de los activos financieros')

        total_assets = pd.DataFrame({'año': balance_sheet['year'],
                                     'Activos': balance_sheet['TOTAL ACTIVO'] / 1000})

        fig_total_assets = px.bar(total_assets, x='año', y='Activos',
                                  labels={'año': 'Año', 'Activos': unidades + moneda},
                                  text_auto=',.0f',
                                  title='Total de activos financieros')

        st.plotly_chart(fig_total_assets, use_container_width=True)

        # Composición de los activos financieros

        assets_summary = pd.DataFrame(
            {'año': balance_sheet['year'],
             'Activo corriente': balance_sheet['Total activo corriente'] / 1000,
             'Activo no corriente': balance_sheet['Total activo no corriente'] / 1000}
        )

        fig_assets = px.bar(assets_summary, x='año', y=['Activo corriente', 'Activo no corriente'], labels={'año': 'Año'}, text_auto=',.0f')

        fig_assets.update_layout(yaxis_title=unidades + moneda, title='Composición de los activos financieros', legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))

        st.plotly_chart(fig_assets, use_container_width=True)

        # RESUMEN DE LOS PASIVOS FINANCIEROS

        st.subheader('Resumen de los pasivos financieros')

        total_liabilities = pd.DataFrame({'año': balance_sheet['year'],
                                          'Pasivos': balance_sheet['TOTAL PASIVO'] / 1000})

        fig_total_liabilities = px.bar(
            total_liabilities,
            x='año',
            y='Pasivos',
            labels={'año': 'Año', 'Pasivos': 'En millones de US$'},
            text_auto=',.0f',
            title='Total de pasivos financieros')

        st.plotly_chart(fig_total_liabilities, use_container_width=True)

        # Composición de los pasivos financieros

        liabilities_summary = pd.DataFrame({'año': balance_sheet['year'],
                                            'Pasivo corriente': balance_sheet['Total pasivo corriente'] / 1000,
                                            'Pasivo no corriente': balance_sheet['Total pasivo no corriente'] / 1000
                                            })

        fig_liabilities = px.bar(
            liabilities_summary,
            x='año',
            y=['Pasivo corriente', 'Pasivo no corriente'],
            labels={'año': 'Año'},
            text_auto=',.0f',
            title='Composición de los pasivos financieros')

        fig_liabilities.update_layout(yaxis_title='En millones de US$',
                                      legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))

        st.plotly_chart(fig_liabilities, use_container_width=True)

        # SUMMARY OF EQUITY

        st.subheader('Resumen del patrimonio')

        total_equity = pd.DataFrame(
            {'año': balance_sheet['year'],
             'Patrimonio': balance_sheet['TOTAL PATRIMONIO'] / 1000}
        )

        fig_total_equity = px.bar(
            total_equity,
            x='año',
            y='Patrimonio',
            labels={'año': 'Año','Patrimonio': 'En millones de US$'},
            text_auto=',.0f',
            title='Total de patrimonio'
        )

        st.plotly_chart(fig_total_equity, use_container_width=True)

    # ASSETS

    elif sidebar_balance == 'Situación de los activos':

        st.title('Situación de los activos financieros al ' + str(year_latest) + ' (en ' + unidades_corto + moneda + ')')

        # SOME KPI's

        latest_assets = balance_sheet['TOTAL ACTIVO'].iloc[-1] / 1000

        assets_t1 = balance_sheet['TOTAL ACTIVO'].iloc[-2] / 1000

        delta_assets = latest_assets / assets_t1 - 1

        delta_assets = '{:.1%}'.format(delta_assets)

        activo_corr_latest = balance_sheet['Total activo corriente'].iloc[-1] / 1000

        activo_corr_t1 = balance_sheet['Total activo corriente'].iloc[-2] / 1000

        delta_act_corr = activo_corr_latest / activo_corr_t1 - 1

        delta_act_corr = '{:.1%}'.format(delta_act_corr)

        activo_no_corr_latest = balance_sheet['Total activo no corriente'].iloc[-1] / 1000

        activo_no_corr_t1 = balance_sheet['Total activo no corriente'].iloc[-2] / 1000

        delta_act_no_corr = activo_no_corr_latest / activo_no_corr_t1 - 1

        delta_act_no_corr = '{:.1%}'.format(delta_act_no_corr)

        kpi_assets1, kpi_assets2, kpi_assets3 = st.columns(3)

        kpi_assets1.metric("Activos (MM US$)", f'{latest_assets:,.0f}', delta_assets)

        kpi_assets2.metric('Activos corrientes (MM US$)', f'{activo_corr_latest:,.0f}', delta_act_corr)

        kpi_assets3.metric('Activos no corrientes (MM US$)', f'{activo_no_corr_latest:,.0f}', delta_act_no_corr)

        # Activo corriente

        st.subheader('Activo corriente')

        # Caja

        assets_cash = pd.DataFrame({'año': balance_sheet['year'],
                                    'Efectivo y equivalentes de efectivo':
            balance_sheet['Efectivo y equivalente de efectivo'] / 1000})

        fig_cash = px.bar(assets_cash, x = 'año', y = 'Efectivo y equivalentes de efectivo',
                       labels = {'año': 'Año',
                                 'Efectivo y equivalentes de efectivo': 'En millones de US$'},
                          title = 'Efectivo y equivalentes de efectivo', text_auto = ',.0f')

        st.plotly_chart(fig_cash, use_container_width = True)

        # Cuentas por cobrar

        ctas_cobrar = pd.DataFrame({
            'año': balance_sheet['year'],
            'Cuentas por cobrar': (balance_sheet['Cuentas por cobrar comerciales'] +
                                  balance_sheet['Otras cuentas por cobrar']) / 1000
        })

        fig_ctas_cobrar = px.bar(ctas_cobrar, x = 'año', y = 'Cuentas por cobrar',
                                 labels = {'año': 'Año', 'Cuentas por cobrar': 'En millones de US$'},
                                 title = 'Cuentas por cobrar 1/', text_auto = ',.0f'
                                 )

        st.plotly_chart(fig_ctas_cobrar, use_container_width = True)

        st.caption('1/ Cuentas por cobrar incluye: (i) Cuentas por cobrar comerciales; y '
                   '(ii) Otras cuentas por cobrar')

        # Inventario

        inventario = pd.DataFrame({
            'año': balance_sheet['year'],
            'Inventarios': balance_sheet['Inventarios'] / 1000
        })

        fig_inventario = px.bar(inventario, x = 'año', y = 'Inventarios',
                                 labels = {'año': 'Año', 'Inventarios': 'En millones de US$'},
                                 title = 'Inventarios', text_auto = ',.0f'
                                 )

        st.plotly_chart(fig_inventario, use_container_width = True)

        # Otros activos corrientes

        otros_act_corr = pd.DataFrame({
            'año': balance_sheet['year'],
            'Otros activos corrientes': (balance_sheet['Otros activos financieros al costo amortizado'] +
                                   balance_sheet['Otros activos'] + balance_sheet['Activos mantenidos para la venta']) / 1000
        })

        fig_otros_act_corr = px.bar(otros_act_corr, x = 'año', y = 'Otros activos corrientes',
                                 labels = {'año': 'Año', 'Otros activos corrientes': 'En millones de US$'},
                                 title = 'Otros activos corrientes 1/', text_auto = ',.0f'
                                 )

        st.plotly_chart(fig_otros_act_corr, use_container_width = True)

        st.caption('1/ Otros activos corrientes incluye: (i) Otros activos financieros al costo amortizado; '
                   '(ii) Otros activos; y (iii) Activos mantenidos para la venta.')

        # Activo no corriente

        st.subheader('Activo no corriente')
        
        # Propiedad, planta y equipo
        
        prop_plant_eq = pd.DataFrame({
            'año': balance_sheet['year'],
            'Propiedad, planta y equipo': balance_sheet['Propiedad, planta y equipo'] / 1000
        })

        fig_prop_plant_eq = px.bar(prop_plant_eq, x = 'año', y = 'Propiedad, planta y equipo',
                                labels = {'año': 'Año', 'Propiedad, planta y equipo': 'En millones de US$'},
                                title = 'Propiedad, planta y equipo', text_auto = ',.0f'
                                )

        st.plotly_chart(fig_prop_plant_eq, use_container_width = True)

        # Otras cuentas por cobrar

        otras_ctas_cobrar = pd.DataFrame({
            'año': balance_sheet['year'],
            'Otras cuentas por cobrar': balance_sheet['Otras cuentas por cobrar no corrientes'] / 1000
        })

        fig_otras_ctas_cobrar = px.bar(otras_ctas_cobrar, x = 'año', y = 'Otras cuentas por cobrar',
                                   labels = {'año': 'Año', 'Otras cuentas por cobrar': 'En millones de US$'},
                                   title = 'Otras cuentas por cobrar', text_auto = ',.0f'
                                   )

        st.plotly_chart(fig_otras_ctas_cobrar, use_container_width = True)

        # Otros activos no corrientes

        otros_act_no_corr = pd.DataFrame({
            'año': balance_sheet['year'],
            'Otros activos no corrientes': (balance_sheet['Otros activos no corrientes'] +
                                            balance_sheet['Propiedades de inversión'] +
                                            balance_sheet['Activos intangibles'] +
                                            balance_sheet['Activos por derecho de uso']) / 1000
        })

        fig_otros_act_no_corr = px.bar(otros_act_no_corr, x = 'año', y = 'Otros activos no corrientes',
                                       labels = {'año': 'Año',
                                                 'Otros activos no corrientes': 'En millones de US$'},
                                       title = 'Otros activos no corrientes 1/', text_auto = ',.0f'
                                       )

        st.plotly_chart(fig_otros_act_no_corr, use_container_width = True)

        st.caption('1/ Otros activos no corrientes incluye: (i) Otros activos no corrientes; '
                   '(ii) Propiedades de inversión; (iii) Activos intangibles; y '
                   '(iv) Activos por derecho de uso.')

    # LIABILITIES

    elif sidebar_balance == 'Situación de los pasivos':

        # SOME KPI's

        st.title('Situación de los pasivos financieros al ' + str(year_latest) + ' (en ' + unidades_corto + moneda + ')')

        latest_liabilities = balance_sheet['TOTAL PASIVO'].iloc[-1] / 1000

        liabilities_t1 = balance_sheet['TOTAL PASIVO'].iloc[-2] / 1000

        delta_liabilities = latest_liabilities / liabilities_t1 - 1

        delta_liabilities = '{:.1%}'.format(delta_liabilities)

        pasivos_corr_latest = balance_sheet['Total pasivo corriente'].iloc[-1] / 1000

        pasivos_corr_t1 = balance_sheet['Total pasivo corriente'].iloc[-2] / 1000

        delta_pas_corr = pasivos_corr_latest / pasivos_corr_t1 - 1

        delta_pas_corr = '{:.1%}'.format(delta_pas_corr)

        pasivos_no_corr_latest = balance_sheet['Total pasivo no corriente'].iloc[-1] / 1000

        pasivos_no_corr_t1 = balance_sheet['Total pasivo no corriente'].iloc[-2] / 1000

        delta_pas_no_corr = pasivos_no_corr_latest / pasivos_no_corr_t1 - 1

        delta_pas_no_corr = '{:.1%}'.format(delta_pas_no_corr)

        kpi_liab1, kpi_liab2, kpi_liab3 = st.columns(3)

        kpi_liab1.metric("Pasivos (MM US$)", f'{latest_liabilities:,.0f}', delta_liabilities, delta_color = 'inverse')

        kpi_liab2.metric("Pasivos corrientes (MM US$)", f'{pasivos_corr_latest:,.0f}', delta_pas_corr, delta_color = 'inverse')

        kpi_liab3.metric("Pasivos no corrientes (MM US$)", f'{pasivos_no_corr_latest:,.0f}', delta_pas_no_corr, delta_color = 'inverse')

        # Pasivos corrientes

        st.subheader('Pasivos corrientes')

        # Cuentas por pagar

        ctas_pagar = pd.DataFrame({
            'año': balance_sheet['year'],
            'Cuentas por pagar': (balance_sheet['Cuentas por pagar comerciales'] +
                                  balance_sheet['Otras cuentas por pagar comerciales']) / 1000
        })

        fig_ctas_pagar = px.bar(ctas_pagar, x = 'año', y = 'Cuentas por pagar',
                                       labels = {'año': 'Año',
                                                 'Cuentas por pagar': 'En millones de US$'},
                                       title = 'Cuentas por pagar 1/', text_auto = ',.0f'
                                       )

        st.plotly_chart(fig_ctas_pagar, use_container_width = True)

        st.caption('1/ Cuentas por pagar incluye: (i) Cuentas por pagar comerciales; y '
                   '(ii) Otras cuentas por pagar comerciales.')

        # Otros pasivos financieros

        otros_pasivos = pd.DataFrame({
            'año': balance_sheet['year'],
            'Otros pasivos financieros': (balance_sheet['Otros pasivos financieros'] +
                                  balance_sheet['Otras provisiones'] +
                                          balance_sheet['Pasivos por arrendamientos']) / 1000
        })

        fig_otros_pasivos = px.bar(otros_pasivos, x = 'año', y = 'Otros pasivos financieros',
                                labels = {'año': 'Año',
                                          'Otros pasivos financieros': 'En millones de US$'},
                                title = 'Otros pasivos financieros 1/', text_auto = ',.0f'
                                )

        st.plotly_chart(fig_otros_pasivos, use_container_width = True)

        st.caption('1/ Otros pasivos financieros incluye: (i) Otros pasivos financieros; '
                   '(ii) Otras provisiones; y (iii) Pasivos por arrendamientos.')

        # Pasivos no corrientes

        st.subheader('Pasivos no corrientes')

        # Pasivos por impuestos diferidos

        impuestos_diferidos = pd.DataFrame({
            'año': balance_sheet['year'],
            'Pasivos por impuestos diferidos': balance_sheet['Pasivos por impuestos diferidos'] / 1000
        })

        fig_impuestos_diferidos = px.bar(impuestos_diferidos, x = 'año', y = 'Pasivos por impuestos diferidos',
                                   labels = {'año': 'Año',
                                             'Pasivos por impuestos diferidos': 'En millones de US$'},
                                   title = 'Pasivos por impuestos diferidos', text_auto = ',.0f'
                                   )

        st.plotly_chart(fig_impuestos_diferidos, use_container_width = True)

        # Otros pasivos no corrientes

        otros_pasivos_no_corr = pd.DataFrame({
            'año': balance_sheet['year'],
            'Otros pasivos no corrientes': (balance_sheet['Otros pasivos financieros no corrientes'] +
                                          balance_sheet['Provisiones'] +
                                          balance_sheet['Pasivos por arrendamientos no corrientes']) / 1000
        })

        fig_otros_pasivos_no_corr = px.bar(otros_pasivos_no_corr, x = 'año', y = 'Otros pasivos no corrientes',
                                   labels = {'año': 'Año',
                                             'Otros pasivos no corrientes': 'En millones de US$'},
                                   title = 'Otros pasivos no corrientes 1/', text_auto = ',.0f'
                                   )

        st.plotly_chart(fig_otros_pasivos_no_corr, use_container_width = True)

        st.caption('1/ Otros pasivos no corrientes incluye: (i) Otros pasivos financieros no corrientes; '
                   '(ii) Provisiones; y (iii) Pasivos por arrendamientos no corrientes.')

    # EQUITY

    elif sidebar_balance == 'Situación del patrimonio':

        st.title('Situación del patrimonio al ' + str(year_latest) + ' (en ' + unidades_corto + moneda + ')')

        # SOME KPI's

        latest_equity = balance_sheet['TOTAL PATRIMONIO'].iloc[-1] / 1000

        equity_t1 = balance_sheet['TOTAL PATRIMONIO'].iloc[-2] / 1000

        delta_equity = latest_equity / equity_t1 - 1

        delta_equity = '{:.1%}'.format(delta_equity)

        capital_latest = (balance_sheet['Capital social'].iloc[-1] +
                          balance_sheet['Capital adicional'].iloc[-1]) / 1000

        capital_t1 = (balance_sheet['Capital social'].iloc[-2] +
                          balance_sheet['Capital adicional'].iloc[-2]) / 1000

        delta_capital = capital_latest / capital_t1 - 1

        delta_capital = '{:.1%}'.format(delta_capital)

        resultados_latest = balance_sheet['Resultados acumulados'].iloc[-1] / 1000

        resultados_t1 = balance_sheet['Resultados acumulados'].iloc[-2] / 1000

        delta_resultados = resultados_latest / resultados_t1 - 1

        delta_resultados = '{:.1%}'.format(delta_resultados)

        kpi_equity1, kpi_equity2, kpi_equity3 = st.columns(3)

        kpi_equity1.metric("Patrimonio (MM US$)", f'{latest_equity:,.0f}', delta_equity)

        kpi_equity2.metric("Capital (MM US$)", f'{capital_latest:,.0f}', delta_capital)

        kpi_equity3.metric("Resultados acumulados (MM US$)", f'{resultados_latest:,.0f}', delta_resultados)

        # Capital

        capital = pd.DataFrame({
            'año': balance_sheet['year'],
            'Capital': (balance_sheet['Capital social'] +
                                            balance_sheet['Capital adicional']) / 1000
        })

        fig_capital = px.bar(capital, x = 'año', y = 'Capital',
                                           labels = {'año': 'Año',
                                                     'Capital': unidades + moneda},
                                           title = 'Capital 1/', text_auto = ',.0f'
                                           )

        st.plotly_chart(fig_capital, use_container_width = True)

        st.caption('1/ Capital incluye: (i) Capital social; y '
                   '(ii) Capital adicional.')

        # Resultados acumulados

        resultados_acum = pd.DataFrame({
            'año': balance_sheet['year'],
            'Resultados acumulados': (balance_sheet['Resultados acumulados']) / 1000
        })

        fig_resultados_acum = px.bar(resultados_acum, x = 'año', y = 'Resultados acumulados',
                             labels = {'año': 'Año',
                                       'Resultados acumulados': unidades + moneda},
                             title = 'Resultados acumulados', text_auto = ',.0f'
                             )

        st.plotly_chart(fig_resultados_acum, use_container_width = True)

        # Reserva legal

        reservas = pd.DataFrame({
            'año': balance_sheet['year'],
            'Reservas del patrimonio': (balance_sheet['Reserva legal'] +
                        balance_sheet['Otras reservas del patrimonio']) / 1000
        })

        fig_reservas = px.bar(reservas, x = 'año', y = 'Reservas del patrimonio',
                             labels = {'año': 'Año',
                                       'Reservas del patrimonio': unidades + moneda},
                             title = 'Reservas del patrimonio 1/', text_auto = ',.0f'
                             )

        st.plotly_chart(fig_reservas, use_container_width = True)

        st.caption('1/ Reservas del patrimonio incluye: (i) Reserva legal; y '
                   '(ii) Otras reservas del patrimonio.')

################################
    
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
                                  title='Prueba defensiva', text_auto = '.1%')

        st.plotly_chart(fig_prueba_defensiva, use_container_width=True)

        st.latex(r'''Prueba\;defensiva = \frac{Caja}{Pasivos\;corrientes}\%
        ''')

        # Capital de trabajo

        st.subheader('4. Capital de trabajo')

        capital_trabajo = pd.DataFrame({'año': assets_summary['año'],
                                        'Capital de trabajo': (balance_sheet['Total activo corriente'] -
                                                            balance_sheet['Total pasivo corriente']) / 1000
                                        })

        fig_capital_trabajo = px.bar(capital_trabajo, x = 'año', y = 'Capital de trabajo',
                                      labels = {'año': 'Año', 'Capital de trabajo': 'En millones de US$'},
                                      title='Capital de trabajo', text_auto = ',.1f')

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

        st.subheader('1. Ingresos totales')

        ingresos_totales = pd.DataFrame({
            'año': assets_summary['año'], 'Ingresos totales': income_statement['Total ingresos'] / 1000
        })

        fig_ingresos_totales = px.bar(ingresos_totales, x = 'año', y = 'Ingresos totales',
                                      labels = {'año': 'Año', 'Ingresos totales': 'Millones de US$'},
                                      title = 'Ingresos totales (en millones de US$)',
                                      text_auto = ',.1f')

        st.plotly_chart(fig_ingresos_totales, use_container_width = True)

        # Margen bruto

        st.subheader('2. Margen bruto')

        margen_bruto = pd.DataFrame({
            'año': assets_summary['año'], 'Margen bruto': income_statement['Ganancia bruta'] /
                                                     income_statement['Total ingresos']
        })

        fig_margen_bruto = px.bar(margen_bruto, x = 'año', y = 'Margen bruto',
                                  labels = {'año': 'Año', 'Margen bruto': '%'},
                                  title = 'Margen bruto (en %)', text_auto = '.1%')

        st.plotly_chart(fig_margen_bruto, use_container_width = True)

        st.latex(r'''Margen\;bruto = \frac{Resultado\;bruto}{Ingresos}\%
        ''')

        # Margen operativo

        st.subheader('3. Margen operativo')

        margen_operativo = pd.DataFrame({
            'año': assets_summary['año'], 'Margen operativo': income_statement['(Pérdida) Ganancia por '
                                                                               'actividades de operación'] /
                                                          income_statement['Total ingresos']
        })

        fig_margen_operativo = px.bar(margen_operativo, x = 'año', y = 'Margen operativo',
                                  labels = {'año': 'Año', 'Margen operativo': '%'},
                                  title = 'Margen operativo (en %)', text_auto = '.1%')

        st.plotly_chart(fig_margen_operativo, use_container_width = True)

        st.latex(r'''Margen\;operativo = \frac{Resultado\;operativo}{Ingresos}\%
        ''')

        # Margen neto

        st.subheader('4. Margen neto')

        margen_neto = pd.DataFrame({
            'año': assets_summary['año'], 'Margen neto': income_statement['Total resultados integrales'] /
                                                    income_statement['Total ingresos']
        })

        fig_margen_neto = px.bar(margen_neto, x = 'año', y = 'Margen neto',
                                 labels = {'año': 'Año', 'Margen neto': '%'},
                                 title = 'Margen neto (en %)', text_auto = '.1%')

        st.plotly_chart(fig_margen_neto, use_container_width = True)

        st.latex(r'''Margen\;neto = \frac{Resultado\;neto}{Ingresos}\%
        ''')

        # ROA

        st.subheader('5. ROA (Return Over Assets)')

        roa = pd.DataFrame({
            'año': assets_summary['año'], 'ROA': income_statement['Total resultados integrales'] /
                                                         balance_sheet['TOTAL ACTIVO']
        })

        fig_roa = px.bar(roa, x = 'año', y = 'ROA',
                                 labels = {'año': 'Año', 'ROA': '%'},
                                 title = 'ROA (Return Over Assets)', text_auto = '.1%')

        st.plotly_chart(fig_roa, use_container_width = True)

        st.latex(r'''ROA\;(Return\;over\;assets) = \frac{Resultado\;neto}{Activos}\%
        ''')

        # ROE

        st.subheader('6. ROE (Return Over Equity)')

        roe = pd.DataFrame({
            'año': assets_summary['año'], 'ROE': income_statement['Total resultados integrales'] /
                                                 balance_sheet['TOTAL PATRIMONIO']
        })

        fig_roe = px.bar(roe, x = 'año', y = 'ROE',
                         labels = {'año': 'Año', 'ROE': '%'},
                         title = 'ROE (Return Over Equity)', text_auto = '.1%')

        st.plotly_chart(fig_roe, use_container_width = True)

        st.latex(r'''ROA\;(Return\;over\;equity) = \frac{Resultado\;neto}{Patrimonio}\%
        ''')

# ESTADO DE RESULTADOS

elif sidebar_options == 'Estado de Resultados':

    st.title('Análisis de los Estados Financieros de Petroperú')

    st.write('Introducir algún comentario sobre los Estados financieros de Petroperú')

    inc_stmt = pd.DataFrame({
        'Componentes': [
            'Ingresos ordinarios',
            'Otros ingresos',
            'Costo de ventas',
            'Gastos de operación',
            'Gastos financieros',
            'Impuestos',
            'Resultado del ejercicio'
                        ],
        'Valores': [
            income_statement['Ingresos de actividades ordinarias'].iloc[-1] / 1000,
            income_statement['Otros ingresos operacionales'].iloc[-1] / 1000,
            income_statement['Costo de ventas'].iloc[-1] / 1000,
            income_statement['Total gastos de operación'].iloc[-1] / 1000,
            (income_statement['Ingresos financieros'].iloc[-1] +
            income_statement['Gastos financieros'].iloc[-1] +
            income_statement['Diferencia de cambio neta'].iloc[-1]) / 1000,
            income_statement['Gasto por impuesto a las ganancias'].iloc[-1] / 1000,
            income_statement['Total resultados integrales'].iloc[-1] / 1000
        ]
    })

    ing_act_ord = income_statement['Ingresos de actividades ordinarias'].iloc[-1] / 1000

    #ing_act_ord = '{:0f}'.format(ing_act_ord)

    ot_ing_op = income_statement['Otros ingresos operacionales'].iloc[-1] / 1000

    #ot_ing_op = '{:0n}'.format(ot_ing_op)

    costo_ventas = income_statement['Costo de ventas'].iloc[-1] / 1000

    #costo_ventas = '{:0n}'.format(costo_ventas)

    gastos_operacion = income_statement['Total gastos de operación'].iloc[-1] / 1000

    #gastos_operacion = '{:0n}'.format(gastos_operacion)

    gastos_fin = (income_statement['Ingresos financieros'].iloc[-1] +
                  income_statement['Gastos financieros'].iloc[-1] +
                  income_statement['Diferencia de cambio neta'].iloc[-1]) / 1000

    #gastos_fin = '{:0n}'.format(gastos_fin)

    impuesto_ganancias = income_statement['Gasto por impuesto a las ganancias'].iloc[-1] / 1000

    #impuesto_ganancias = '{:0n}'.format(impuesto_ganancias)

    resultado_neto = income_statement['Total resultados integrales'].iloc[-1] / 1000

    #resultado_neto = '{:0n}'.format(resultado_neto)

    fig_inc_stmt = go.Figure(go.Waterfall(
        orientation = "v",
        base = 0,
        measure = ['absolute', 'relative', 'relative', 'relative', 'relative', 'relative', 'total'],
        x = [
            'Ingresos ordinarios',
            'Otros ingresos',
            'Costo de ventas',
            'Gastos de operación',
            'Gastos financieros',
            'Impuestos',
            'Resultado del ejercicio'],
        text = [ing_act_ord, ot_ing_op, costo_ventas, gastos_operacion, gastos_fin, impuesto_ganancias, resultado_neto],
        textposition = 'outside',
        y = [ing_act_ord, ot_ing_op, costo_ventas, gastos_operacion, gastos_fin, impuesto_ganancias, resultado_neto]
    ))

    fig_inc_stmt.update_layout(
        title = 'Estado de resultados de ' + empresa + ' para el año ' + str(year_latest),
        showlegend = False
    )

    st.plotly_chart(fig_inc_stmt, use_container_width = False, height = 4800, width = 4000)

# FLUJO DE EFECTIVO

elif sidebar_options == 'Flujo de efectivo':

    st.title('Análisis del flujo de efectivo de Petroperú')

    st.write('Introducir algún comentario sobre el Flujo de efectivo de Petroperú')

# NORMAS LEGALES

elif sidebar_options == 'Normas legales':

    st.title('Normas legales')

    st.write('Principales normas legales relacionadas a Petroperú y el PMRT.')
