import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Bidirectional
from tensorflow.keras.callbacks import EarlyStopping
import plotly.graph_objects as go

### UI STYLING ###
st.markdown("""
<style>
.title-font {font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; font-size: 48px; font-weight: bold; color: #ffffff;}
.subtitle-font {font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; font-size: 48px; color: #f88181;}
.stSlider label, .stSelectbox label, .stMultiSelect label, .stTextInput label,
.stNumberInput label, .stFileUploader label, .stCheckbox label, .stRadio label,
.stDateInput label, .stColorPicker label, .stTimeInput label {
    color: white !important;
    font-weight: bold;
}
.stSlider > div > div {
    color: white;
}
.stSelectbox div[data-baseweb="select"] {
    color: black;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title-font">TIME SERIES</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-font">Forecaster</div>', unsafe_allow_html=True)
st.markdown('<hr style="border: none; height: 4px; background-color: white; margin: 10px 0;">', unsafe_allow_html=True)

### BUTTONS ###
if "selected_section" not in st.session_state:
    st.session_state.selected_section = "Predictor"

def set_section(section_name):
    st.session_state.selected_section = section_name

col1, col2 = st.columns([1, 1])
with col1:
    st.button("Time Series Forecaster", key="btn_time_series_forecaster", on_click=set_section, args=("Time Series Forecaster",))
with col2:
    st.button("Description", key="btn_times_series_forecaster_description", on_click=set_section, args=("Time Series Forecaster Description",))

st.markdown("""<style>
    div[data-testid="stButton"] > button {color: white !important; background-color: #ff5757 !important; border-radius: 8px !important;
                                          font-weight: bold !important; font-size: 18px !important; padding: 10px 30px !important; 
                                          width: 100% !important; height: 50px !important; border: none !important; cursor: pointer;
                                          transition: background-color 0.3s ease !important;}

    div[data-testid="stButton"] > button:hover {background-color: #e04e4e !important;}
    /* Target the file size text next to uploaded file name */
    [data-testid="stFileUploader"] small {
        color: gray !important;
        font-size: 14px !important;  /* Optional: adjust size */
        font-weight: 500 !important; /* Optional: adjust weight */
    } 
    </style>""", unsafe_allow_html=True)

if st.session_state.selected_section != "Time Series Forecaster Description":
    st.title("Forecaster")
    uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx", "xls"])

    if uploaded_file:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            xls = pd.ExcelFile(uploaded_file)
            sheet = st.selectbox("Select Excel sheet", xls.sheet_names)
            df = pd.read_excel(xls, sheet_name=sheet)

        st.write("Preview of your data:")
        st.dataframe(df)

        datetime_col = st.selectbox("Select date column", df.columns)
        try:
            df[datetime_col] = pd.to_datetime(df[datetime_col])
        except Exception as e:
            st.error(f"Error converting column '{datetime_col}' to datetime: {e}")
            st.stop()

        df.set_index(datetime_col, inplace=True)
        df.sort_index(inplace=True)

        target_col = st.selectbox("Select target column to forecast", df.columns)
        feature_cols = st.multiselect("Select additional features (optional)", df.columns.drop(target_col))

        ### SIDEBAR CONFIG ###
        st.sidebar.header("Model Parameters")
        time_steps = st.sidebar.slider("Time steps (input window)", 2, 250, 1)
        forecast_horizon = st.sidebar.slider("Time steps to predict", 1, 250, 1)
        lstm_units = st.sidebar.slider("LSTM units", 1, 250, 1)
        num_layers = st.sidebar.slider("Number of LSTM layers", 1, 10, 1)
        dropout_rate = st.sidebar.slider("Dropout rate", 0.0, 0.99, 0.0, step=0.01)
        epochs = st.sidebar.slider("Epochs", 1, 250, 1)
        early_stopping_patience = st.sidebar.slider("Early Stopping Patience", 1, 50, 5)
        loss_function_before_formatting = st.sidebar.radio("Select Loss Function", ["MAE", "RMSE", "MAPE"])
        loss_function = loss_function_before_formatting.lower()
        
        ### TRAIN BUTTON ###
        if st.button("Train & Forecast"):
            try:
                data = df[[target_col] + feature_cols]
                scaler = MinMaxScaler()
                data_scaled = scaler.fit_transform(data)

                if len(data_scaled) - time_steps - forecast_horizon + 1 <= 0:
                    st.error("Not enough data for the chosen time steps and forecast horizon.")
                    st.stop()

                def create_sequences(data, time_steps, horizon):
                    X, y = [], []
                    for i in range(len(data) - time_steps - horizon + 1):
                        seq_x = data[i:i + time_steps]
                        if seq_x.ndim == 1:
                            seq_x = seq_x.reshape(-1, 1)
                        X.append(seq_x)
                        y.append(data[i + time_steps:i + time_steps + horizon, 0])
                    return np.array(X), np.array(y)

                X, y = create_sequences(data_scaled, time_steps, forecast_horizon)
                split_idx = int(len(X) * 0.8)
                X_train, X_val = X[:split_idx], X[split_idx:]
                y_train, y_val = y[:split_idx], y[split_idx:]

                if len(X_train) == 0 or len(y_train) == 0:
                    st.error("Training data is empty after creating sequences. Adjust time steps or forecast horizon.")
                    st.stop()

                ###  BUILD MODEL ###
                model = Sequential()
                for i in range(num_layers):
                    return_seq = (i < num_layers - 1)
                    if i == 0:
                        model.add(Bidirectional(LSTM(units=lstm_units, return_sequences=return_seq), input_shape=(X.shape[1], X.shape[2])))
                    else:
                        model.add(Bidirectional(LSTM(units=lstm_units, return_sequences=return_seq)))
                    model.add(Dropout(dropout_rate))
                model.add(Dense(forecast_horizon))
                model.compile(optimizer='adam', loss=loss_function)

                ### EARLY STOPPING ###
                early_stopping = EarlyStopping(monitor='val_loss', patience=early_stopping_patience, restore_best_weights=True)

                ### TRAIN MODEL ###
                with st.spinner("Training the model..."):
                    history = model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=epochs, verbose=0, callbacks=[early_stopping])

                st.success(f"Training successfully executed. Training has been stopped after {len(history.history['loss'])} epochs due to early stopping.")

                def safe_mean_absolute_percentage_error(y_true, y_pred):
                    mask = y_true != 0
                    if np.sum(mask) == 0:
                        return None
                    return np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100

                ### METRICS ###
                y_train_pred = model.predict(X_train)
                y_val_pred = model.predict(X_val)

                train_mae = mean_absolute_error(y_train, y_train_pred)
                train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
                train_mape = safe_mean_absolute_percentage_error(y_train, y_train_pred)

                val_mae = mean_absolute_error(y_val, y_val_pred)
                val_rmse = np.sqrt(mean_squared_error(y_val, y_val_pred))
                val_mape = safe_mean_absolute_percentage_error(y_val, y_val_pred)

                st.subheader("Training & Validation Error Metrics")
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Training**")
                    st.write(f"MAE: {train_mae:.4f}")
                    st.write(f"RMSE: {train_rmse:.4f}")
                    st.write(f"MAPE: {train_mape:.2f}%" if train_mape else "MAPE: -")
                with col2:
                    st.markdown("**Validation**")
                    st.write(f"MAE: {val_mae:.4f}")
                    st.write(f"RMSE: {val_rmse:.4f}")
                    st.write(f"MAPE: {val_mape:.2f}%" if val_mape else "MAPE: -")

                ### LOSS PLOT ###
                fig_loss = go.Figure()
                fig_loss.add_trace(go.Scatter(y=history.history['loss'], name=f'Training {loss_function_before_formatting}', line=dict(color="#1AAAFE", width=3)))
                fig_loss.add_trace(go.Scatter(y=history.history['val_loss'], name=f'Validation {loss_function_before_formatting}', line=dict(color="#ff5757", width=3)))
                fig_loss.update_layout(title={"text": f"Training vs Validation {loss_function_before_formatting}", "x": 0.5, "font": {"size": 24, "color": "white"}},
                                    xaxis={"title": {"text": "Epoch", "font": {"size": 15, "color": "white"}}, "tickfont": {"color": "white"}},
                                    yaxis={"title": {"text": "Loss", "font": {"size": 15, "color": "white"}}, "tickfont": {"color": "white"}},
                                    plot_bgcolor='#2f2f2f', paper_bgcolor='#2f2f2f', font=dict(color='white'),
                                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color='white')))
                st.plotly_chart(fig_loss, use_container_width=True)

                ### FORECASTING ###
                st.subheader("Actual & Forecasted Values")
                last_seq = data_scaled[-time_steps:].reshape(1, time_steps, -1)
                prediction_scaled = model.predict(last_seq)[0]

                pad_features = np.zeros((forecast_horizon, len(feature_cols)))
                pred_input = np.hstack([prediction_scaled.reshape(-1, 1), pad_features])
                prediction = scaler.inverse_transform(pred_input)[:, 0]

                last_date = df.index[-1]

                inferred_freq = pd.infer_freq(df.index)
                if inferred_freq is None:
                    inferred_freq = st.selectbox("Frequency could not be inferred. Please select the frequency of your time series data:",
                                                ["D", "W", "M", "MS", "H"])

                forecast_index = pd.date_range(start=last_date, periods=forecast_horizon + 1, freq=inferred_freq)[1:]  # skip last_date itself

                hist_x = df.index
                hist_y = df[target_col].values
                forecast_x_full = [last_date] + list(forecast_index)
                forecast_y_full = [hist_y[-1]] + list(prediction)

                fig = go.Figure()
                fig.add_trace(go.Scatter(x=hist_x, y=hist_y, mode='lines', name='Actual', line=dict(color="#ff5757", width=3)))
                fig.add_trace(go.Scatter(x=forecast_x_full, y=forecast_y_full, mode='lines', name='Forecast', line=dict(color="#ff5757", width=3, dash='dash')))
                fig.update_layout(title={"text": f"Actuals & Forecast of {target_col}", "x": 0.5, "font": {"size": 24, "color": "white"}},
                                xaxis={"title": {"text": "Date", "font": {"size": 15, "color": "white"}}, "tickfont": {"color": "white"}},
                                yaxis={"title": {"text": target_col, "font": {"size": 15, "color": "white"}}, "tickfont": {"color": "white"}},
                                plot_bgcolor='#2f2f2f', paper_bgcolor='#2f2f2f', font=dict(color='white'),
                                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color='white')),
                                margin=dict(t=100, b=80, l=60, r=40))
                st.plotly_chart(fig, use_container_width=True)

                forecast_df = pd.DataFrame({f"Forecast ({target_col})": prediction}, index=forecast_index)
                forecast_df.index.name = df.index.name or "Date"
                st.subheader("Forecast Results")
                st.dataframe(forecast_df.style.format(precision=2))

            except Exception as e:
                st.error(f"Training failed with error: {e}")

### DESCRIPTION ###
else:
    st.title("Description of the Project")
    st.markdown("""<div style='color: white;'>
        <p>This forecaster is intended to provide univariate time series predictions. Univariate time series represent such series which involve the prediction of only 1 variable (column). To achieve the forecasting, select file in the CSV or Excel format, in the case of Excel choose the corresponding sheet with the time series data, select the date (time) column, select which column to forecast, optionally add which additionally features should be taken into account during the forecasting which contribute & influence the predicted value. Once the training finishes, you can see the training & validation error metrics as well as the results of the predictions on the line graph. The lower the error metrics, the more accurate predictions will be.</p>
        <p><strong>IT IS CRUCIAL TO SELECT THE RIGHT DATE COLUMN & THE RIGHT COLUMN TO FORECAST!</strong> The date column must contain a date/datetime type.</p>
    </div>""", unsafe_allow_html=True)
