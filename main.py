import pandas as pd

def process_data(file_path):
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"Xəta: Fayl oxunmadı! {e}")
        return

    def check_row(row):
        sub_status = str(row['sub status']).lower().strip()
        req = str(row['req']).lower()
        result = "VALID"
        comment = ""

        if "title" in sub_status:
            title = str(row['title']).lower()
            keywords = [k.strip() for k in req.split(',')]
            if not any(k in title for k in keywords):
                result = "INVALID"
                comment = f"Title does not match keywords: {req}"

        elif "prooflink" in sub_status:
            pl = str(row['prooflink']).lower()
            email_domain = str(row['email']).split('@')[-1] if '@' in str(row['email']) else ""
            is_linkedin = "linkedin.com/in/" in pl 
            is_zoominfo = "zoominfo.com/p/" in pl 
            is_corp_site = email_domain in pl if email_domain else False 
            if not (is_linkedin or is_zoominfo or is_corp_site):
                result = "INVALID"
                comment = "Prooflink is not LinkedIn/ZoomInfo or doesn't match corporate email"

        elif "nwc" in sub_status:
            status_val = str(row['status']).lower().strip()
            if status_val in ['nan', '', 'valid']:
                result = "VALID"
            elif status_val == 'a':
                result = "INVALID"
                comment = "Retired lead"
            elif status_val == '!':
                result = "INVALID"
                comment = "Suspicious lead"
            elif status_val in ['r', 'no info', 'no company match']:
                result = "RECHECK"
                comment = "Manual recheck required"

        else:
            if pd.isna(row['company']) or pd.isna(row['first_name']):
                result = "INVALID"
                comment = "Missing company or person data."

        return pd.Series([result, comment])

    df[['Result', 'Comment']] = df.apply(check_row, axis=1)

    output_name = "Eldar_Result.xlsx"
    df.to_excel(output_name, index=False)
    print(f"Finished the Process.: {output_name}")

# Faylın adını yoxla
process_data('DataCheck_DemoCode.xlsx')