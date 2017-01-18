namespace cpp qfpay

struct EncryptorRet
{
    1: i32 code,
    2: binary data;
}
struct CardIET
{
    1: i32 code,
    2: string cardno;
    3: string expire;
    4: string track2;
    5: string track3;
    6: string real_cardno;
}
struct TokenRet
{
    1: i32 code,
    2: string cardno;
}
struct TckRet
{
    1: i32 code;
    2: binary data;
}
struct SignRet
{
    1: i32 code;
    2: string data;
}
struct GenkeyRet
{
    1: i32 code;
    2: string mackey;
    3: string pinkey1;
    4: string pinkey2;
    5: string tckkey;
}

struct RetTransferKey
{
    1: i32 code;
    2: string transfer_key;
}

struct RetClientSign
{
    1: i32 code;
    2: string sign;
}

struct PinResult
{
    1: i32 code;
    2: string pin;
}

struct Env
{
    1: i32 code;
    2: string env;
    3: string mackey;
    4: string pinkey1;
    5: string pinkey2;
    6: string tck;
}

struct PinkeyRet {
	1: i32 code;
	2: string tsk_pinkey;
	3: string lmk_pinkey;
}

struct TrackRet {
    1: i32 code;
    2: string track2;
    3: string track3;
}

struct ChanpayKeys {
    1:i32 code;
    2:string zpk;
    3:string tdk;
    4:string mackey;
    5:string tmk;
    6:string zpkcheckvalue;
    7:string tdkcheckvalue;
    8:string mackeycheckvalue;
    9:string tmkcheckvalue;
}

struct OrgKeys {
    1:i32 code;
    2:string m_zpk;
    3:string m_zak;
    4:string m_zek;
    5:string l_zpk;
    6:string l_zak;
    7:string l_zek;
    8:string l_enc_pin_key;
}

struct OrgTrackData {
    1:i32 code;
    2:string trackdata;
}

service Encryptor {
    void ping();
    
    OrgKeys     qf_gen_org_key(1:string zmk),
    ChanpayKeys qf_decode_chanpay_keys(1:string tmk, 2:string tdk, 3:string mackey, 4:string pinkey, 5:string zmk),
        
    EncryptorRet qf_mac_generate(1:binary input, 2:string mackey, 3:string bankid, 
        4:string psamid, 5:string random),
    
    EncryptorRet qf_mac_gen_tl(1:binary input, 2:string mackey, 3:string zmk),

    EncryptorRet qf_mac_gen_hy(1:binary input, 2:string mackey, 3:string zmk),
    
    EncryptorRet qf_mac_gen_yibao(1:binary input, 2:string mackey, 3:string zmk),

    TrackRet qf_track_encryptor(1:string track2, 2:string track3, 3:string tdk, 4:string zmk),

    CardIET      qf_cardiet_get(1:binary input, 2:string pinkey, 3:string bankid, 
        4:string psamid, 5:string random),

    EncryptorRet qf_card_enc(1:binary input, 2:string pinkey, 3:string bankid, 
        4:string psamid, 5:string random),

    EncryptorRet qf_pin_exchange(1:binary input, 2:string pinkey, 3:string bankid, 
        4:string psamid, 5:string random, 6:string dzmk, 7:string dzpk, 8:string cardno),

    EncryptorRet qf_pin_exchange_org(1:binary input, 2:string szpk, 3:string dzmk, 4:string dzpk, 5:string cardno),
    
    TckRet       qf_tck_generate(1:string passkey, 2:string tckkey, 3:string diskey,
        4:string fackey, 5:string tid),

    SignRet      qf_pri_sign(1:string abs),

    GenkeyRet    qf_gen_keys(1:string mackey, 2: string pinkey, 3: string tck),

    RetTransferKey  qf_get_tsk(1:string enckey),

    RetClientSign qf_dec_sign(1:string pubenc),

    PinResult    qf_pin_encrypt(1:binary input, 2:string pinkey, 3:string bandid,
        4:string psamid, 5:string random, 6:string cardcd),

    Env          qf_gen_env(1:string diskey, 2:string fackey, 3:string tid, 4:string qpos_pubkey),

    TokenRet     qf_dec_token(1:string cardno, 2:string key),

    TokenRet     qf_enc_token(1:string cardno, 2:string key),

    PinkeyRet    qf_get_pinkey(1:string tsk),

    CardIET      qf_dec_cardiet(1:binary input, 2:string pinkey, 3:string bankid, 4:string psamid, 5:string random),

    TokenRet     qf_enc_cardno(1:string cardno, 2:string key),

    TokenRet     qf_dec_cardno(1:string cardno, 2:string key),
    OrgTrackData qf_zek_de(1:string zek, 2:string trackdata, 3:i32 de_flag), 
}
