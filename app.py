with st.spinner("掃描股票池中..."):

    for code in AI_POOL:

        try:

            df = api.taiwan_stock_daily(
                stock_id=code,
                start_date="2025-01-01"
            )

            if df.empty or len(df) < 60:
                continue

            close = float(df["close"].iloc[-1])

            ma20 = float(
                df["close"].rolling(20).mean().iloc[-1]
            )

            ma60 = float(
                df["close"].rolling(60).mean().iloc[-1]
            )

            volume = float(
                df["Trading_Volume"].iloc[-1]
            )

            vol20 = float(
                df["Trading_Volume"].rolling(20).mean().iloc[-1]
            )

            score = calc_score(
                close,
                ma20,
                ma60,
                volume,
                vol20
            )

            results.append({
                "code": code,
                "score": score,
                "price": round(close, 2),
                "stop": round(ma20, 2),
                "target1": round(close * 1.15, 2),
                "target2": round(close * 1.30, 2)
            })

        except Exception:
            pass
