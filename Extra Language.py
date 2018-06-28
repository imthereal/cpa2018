import json
from multiprocessing.pool import ThreadPool

import requests

locales = ["af", "af-NA", "af-ZA", "agq", "agq-CM", "ak", "ak-GH", "am", "am-ET", "ar", "ar-001", "ar-AE", "ar-BH",
           "ar-DZ", "ar-EG", "ar-IQ", "ar-JO", "ar-KW", "ar-LB", "ar-LY", "ar-MA", "ar-OM", "ar-QA", "ar-SA", "ar-SD",
           "ar-SY", "ar-TN", "ar-YE", "as", "as-IN", "asa", "asa-TZ", "az", "az-Cyrl", "az-Cyrl-AZ", "az-Latn",
           "az-Latn-AZ", "bas", "bas-CM", "be", "be-BY", "bem", "bem-ZM", "bez", "bez-TZ", "bg", "bg-BG", "bm", "bm-ML",
           "bn", "bn-BD", "bn-IN", "bo", "bo-CN", "bo-IN", "br", "br-FR", "brx", "brx-IN", "bs", "bs-BA", "ca", "ca-ES",
           "cgg", "cgg-UG", "chr", "chr-US", "cs", "cs-CZ", "cy", "cy-GB", "da", "da-DK", "dav", "dav-KE", "de",
           "de-AT", "de-BE", "de-CH", "de-DE", "de-LI", "de-LU", "dje", "dje-NE", "dua", "dua-CM", "dyo", "dyo-SN",
           "ebu", "ebu-KE", "ee", "ee-GH", "ee-TG", "el", "el-CY", "el-GR", "en", "en-AS", "en-AU", "en-BB", "en-BE",
           "en-BM", "en-BW", "en-BZ", "en-CA", "en-GB", "en-GU", "en-GY", "en-HK", "en-IE", "en-IN", "en-JM", "en-MH",
           "en-MP", "en-MT", "en-MU", "en-NA", "en-NZ", "en-PH", "en-PK", "en-SG", "en-TT", "en-UM", "en-US",
           "en-US-POSIX", "en-VI", "en-ZA", "en-ZW", "eo", "es", "es-419", "es-AR", "es-BO", "es-CL", "es-CO", "es-CR",
           "es-DO", "es-EC", "es-ES", "es-GQ", "es-GT", "es-HN", "es-MX", "es-NI", "es-PA", "es-PE", "es-PR", "es-PY",
           "es-SV", "es-US", "es-UY", "es-VE", "et", "et-EE", "eu", "eu-ES", "ewo", "ewo-CM", "fa", "fa-AF", "fa-IR",
           "ff", "ff-SN", "fi", "fi-FI", "fil", "fil-PH", "fo", "fo-FO", "fr", "fr-BE", "fr-BF", "fr-BI", "fr-BJ",
           "fr-BL", "fr-CA", "fr-CD", "fr-CF", "fr-CG", "fr-CH", "fr-CI", "fr-CM", "fr-DJ", "fr-FR", "fr-GA", "fr-GF",
           "fr-GN", "fr-GP", "fr-GQ", "fr-KM", "fr-LU", "fr-MC", "fr-MF", "fr-MG", "fr-ML", "fr-MQ", "fr-NE", "fr-RE",
           "fr-RW", "fr-SN", "fr-TD", "fr-TG", "fr-YT", "ga", "ga-IE", "gl", "gl-ES", "gsw", "gsw-CH", "gu", "gu-IN",
           "guz", "guz-KE", "gv", "gv-GB", "ha", "ha-Latn", "ha-Latn-GH", "ha-Latn-NE", "ha-Latn-NG", "haw", "haw-US",
           "he", "he-IL", "hi", "hi-IN", "hr", "hr-HR", "hu", "hu-HU", "hy", "hy-AM", "id", "id-ID", "ig", "ig-NG",
           "ii", "ii-CN", "is", "is-IS", "it", "it-CH", "it-IT", "ja", "ja-JP", "jmc", "jmc-TZ", "ka", "ka-GE", "kab",
           "kab-DZ", "kam", "kam-KE", "kde", "kde-TZ", "kea", "kea-CV", "khq", "khq-ML", "ki", "ki-KE", "kk", "kk-Cyrl",
           "kk-Cyrl-KZ", "kl", "kl-GL", "kln", "kln-KE", "km", "km-KH", "kn", "kn-IN", "ko", "ko-KR", "kok", "kok-IN",
           "ksb", "ksb-TZ", "ksf", "ksf-CM", "kw", "kw-GB", "lag", "lag-TZ", "lg", "lg-UG", "ln", "ln-CD", "ln-CG",
           "lt", "lt-LT", "lu", "lu-CD", "luo", "luo-KE", "luy", "luy-KE", "lv", "lv-LV", "mas", "mas-KE", "mas-TZ",
           "mer", "mer-KE", "mfe", "mfe-MU", "mg", "mg-MG", "mgh", "mgh-MZ", "mk", "mk-MK", "ml", "ml-IN", "mr",
           "mr-IN", "ms", "ms-BN", "ms-MY", "mt", "mt-MT", "mua", "mua-CM", "my", "my-MM", "naq", "naq-NA", "nb",
           "nb-NO", "nd", "nd-ZW", "ne", "ne-IN", "ne-NP", "nl", "nl-AW", "nl-BE", "nl-CW", "nl-NL", "nl-SX", "nmg",
           "nmg-CM", "nn", "nn-NO", "nus", "nus-SD", "nyn", "nyn-UG", "om", "om-ET", "om-KE", "or", "or-IN", "pa",
           "pa-Arab", "pa-Arab-PK", "pa-Guru", "pa-Guru-IN", "pl", "pl-PL", "ps", "ps-AF", "pt", "pt-AO", "pt-BR",
           "pt-GW", "pt-MZ", "pt-PT", "pt-ST", "rm", "rm-CH", "rn", "rn-BI", "ro", "ro-MD", "ro-RO", "rof", "rof-TZ",
           "ru", "ru-MD", "ru-RU", "ru-UA", "rw", "rw-RW", "rwk", "rwk-TZ", "saq", "saq-KE", "sbp", "sbp-TZ", "seh",
           "seh-MZ", "ses", "ses-ML", "sg", "sg-CF", "shi", "shi-Latn", "shi-Latn-MA", "shi-Tfng", "shi-Tfng-MA", "si",
           "si-LK", "sk", "sk-SK", "sl", "sl-SI", "sn", "sn-ZW", "so", "so-DJ", "so-ET", "so-KE", "so-SO", "sq",
           "sq-AL", "sr", "sr-Cyrl", "sr-Cyrl-BA", "sr-Cyrl-ME", "sr-Cyrl-RS", "sr-Latn", "sr-Latn-BA", "sr-Latn-ME",
           "sr-Latn-RS", "sv", "sv-FI", "sv-SE", "sw", "sw-KE", "sw-TZ", "swc", "swc-CD", "ta", "ta-IN", "ta-LK", "te",
           "te-IN", "teo", "teo-KE", "teo-UG", "th", "th-TH", "ti", "ti-ER", "ti-ET", "to", "to-TO", "tr", "tr-TR",
           "twq", "twq-NE", "tzm", "tzm-Latn", "tzm-Latn-MA", "uk", "uk-UA", "ur", "ur-IN", "ur-PK", "uz", "uz-Arab",
           "uz-Arab-AF", "uz-Cyrl", "uz-Cyrl-UZ", "uz-Latn", "uz-Latn-UZ", "vai", "vai-Latn", "vai-Latn-LR", "vai-Vaii",
           "vai-Vaii-LR", "vi", "vi-VN", "vun", "vun-TZ", "xog", "xog-UG", "yav", "yav-CM", "yo", "yo-NG", "zh",
           "zh-Hans", "zh-Hans-CN", "zh-Hans-HK", "zh-Hans-MO", "zh-Hans-SG", "zh-Hant", "zh-Hant-HK", "zh-Hant-MO",
           "zh-Hant-TW", "zu", "zu-ZA"]

print(len(locales))
ignore_locales = ["ar_SA", "cs_CZ", "da_DK", "de_DE", "el_GR", "es_ES", "et_EE", "fi_FI", "fr_FR", "he_IL", "hi_IN",
                  "hu_HU", "id_ID", "it_IT", "ja_JP", "lt_LT", "lv_LV", "my_MM", "nl_NL", "no_NO", "pl_PL", "pt_PT",
                  "pt_BR", "ro_RO", "ru_RU", "sv_SE", "tr_TR", "ur_PK", "zh_CN", "zh_HK", "en"]
print(len(ignore_locales))

s = requests.Session()


def test_locale(locale):
    if (locale.replace('-', '_') not in ignore_locales):
        r = s.get('http://43.241.202.33:3003/i18n/' + locale.replace('-', '_') + '.json')

        try:
            json.loads(r.text)
            # print(locale.replace('-', '_'), r)
            print(r.url)
        except ValueError:
            pass


with ThreadPool(20) as p:
    p.map(test_locale, locales)