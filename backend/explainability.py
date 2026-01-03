"""
Module untuk explainability/interpretability model
Menghasilkan alasan kenapa model memprediksi phishing/genuine
"""

import numpy as np
from typing import Dict

def get_confidence_level(probability: float) -> str:
    """Tentukan level confidence berdasarkan probabilitas"""
    if probability >= 0.8:
        return "sangat tinggi"
    elif probability >= 0.65:
        return "tinggi"
    elif probability >= 0.5:
        return "sedang"
    else:
        return "rendah"

def generate_explanation(label: str, phishing_prob: float, genuine_prob: float) -> Dict[str, str]:
    """
    Generate explanation untuk prediksi
    
    Returns:
        Dict dengan keys: confidence_level, main_reason, details
    """
    is_phishing = label == "phishing"
    main_prob = phishing_prob if is_phishing else genuine_prob
    
    confidence = get_confidence_level(main_prob)
    
    # Generate main reason berdasarkan probabilitas
    if is_phishing:
        if main_prob >= 0.8:
            main_reason = "Model mendeteksi karakteristik visual yang sangat mirip dengan situs phishing"
            details = [
                "Terdapat indikasi pola visual yang umum ditemukan pada situs phishing",
                "Layout atau elemen UI menunjukkan kemiripan dengan situs phishing yang pernah dilatih",
                "Tingkat kepercayaan model: sangat tinggi"
            ]
        elif main_prob >= 0.65:
            main_reason = "Model mendeteksi beberapa karakteristik yang mengindikasikan phishing"
            details = [
                "Terdapat beberapa pola visual yang mencurigakan",
                "Layout atau desain menunjukkan kemiripan dengan situs phishing",
                "Tingkat kepercayaan model: tinggi, namun tetap perlu verifikasi manual"
            ]
        else:
            main_reason = "Model mendeteksi kemungkinan indikasi phishing, namun tidak terlalu kuat"
            details = [
                "Terdapat beberapa karakteristik yang sedikit mencurigakan",
                "Tingkat kepercayaan model: sedang",
                "Sangat disarankan untuk melakukan verifikasi manual yang lebih teliti"
            ]
    else:  # genuine
        if main_prob >= 0.8:
            main_reason = "Model mendeteksi karakteristik visual yang konsisten dengan situs genuine"
            details = [
                "Layout dan desain menunjukkan pola yang umum ditemukan pada situs legitimate",
                "Tidak ada indikasi visual yang mencurigakan",
                "Tingkat kepercayaan model: sangat tinggi"
            ]
        elif main_prob >= 0.65:
            main_reason = "Model mendeteksi karakteristik yang lebih condong ke situs genuine"
            details = [
                "Sebagian besar karakteristik visual menunjukkan pola legitimate",
                "Tingkat kepercayaan model: tinggi",
                "Tetap disarankan untuk melakukan verifikasi URL dan sertifikat SSL"
            ]
        else:
            main_reason = "Model tidak yakin, hasil menunjukkan kemungkinan genuine namun tidak kuat"
            details = [
                "Karakteristik visual tidak terlalu jelas",
                "Tingkat kepercayaan model: sedang",
                "Sangat disarankan untuk melakukan verifikasi manual yang lebih teliti"
            ]
    
    return {
        "confidence_level": confidence,
        "main_reason": main_reason,
        "details": details,
        "recommendation": get_recommendation(is_phishing, main_prob)
    }

def get_recommendation(is_phishing: bool, probability: float) -> str:
    """Generate recommendation berdasarkan prediksi"""
    if is_phishing:
        if probability >= 0.8:
            return "HINDARI memasukkan informasi sensitif. Verifikasi URL, cek domain, dan pastikan sertifikat SSL valid sebelum melanjutkan."
        elif probability >= 0.65:
            return "HATI-HATI. Sebaiknya jangan memasukkan informasi sensitif. Lakukan verifikasi URL dan domain dengan teliti."
        else:
            return "Waspada. Meskipun indikasi tidak terlalu kuat, tetap lakukan verifikasi manual sebelum memasukkan informasi sensitif."
    else:
        if probability >= 0.8:
            return "Situs terlihat legitimate berdasarkan analisis visual. Tetap verifikasi URL dan sertifikat SSL sebelum memasukkan informasi sensitif."
        elif probability >= 0.65:
            return "Situs terlihat legitimate, namun tetap lakukan verifikasi standar (URL, SSL, domain) sebelum memasukkan informasi sensitif."
        else:
            return "Verifikasi manual sangat disarankan. Jangan hanya mengandalkan hasil analisis visual ini."






