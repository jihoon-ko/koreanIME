real_first = "ㄱ ㄲ ㄴ ㄷ ㄸ ㄹ ㅁ ㅂ ㅃ ㅅ ㅆ ㅇ ㅈ ㅉ ㅊ ㅋ ㅌ ㅍ ㅎ".strip().split()
real_second = "ㅏ ㅐ ㅑ ㅒ ㅓ ㅔ ㅕ ㅖ ㅗ ㅘ ㅙ ㅚ ㅛ ㅜ ㅝ ㅞ ㅟ ㅠ ㅡ ㅢ ㅣ".strip().split()
real_third = [None] + ("ㄱ ㄲ ㄳ ㄴ ㄵ ㄶ ㄷ ㄹ ㄺ ㄻ ㄼ ㄽ ㄾ ㄿ ㅀ ㅁ ㅂ ㅄ ㅅ ㅆ ㅇ ㅈ ㅊ ㅋ ㅌ ㅍ ㅎ".strip().split())

second_combine_dict = {
    ('ㅗ','ㅏ'):'ㅘ',
    ('ㅗ','ㅐ'):'ㅙ',
    ('ㅗ','ㅣ'):'ㅚ',
    ('ㅜ','ㅓ'):'ㅝ',
    ('ㅜ','ㅔ'):'ㅞ',
    ('ㅜ','ㅣ'):'ㅟ',
    ('ㅡ','ㅣ'):'ㅢ'
}

third_combine_dict = {
    ('ㄱ','ㅅ'):'ㄳ',
    ('ㄴ','ㅈ'):'ㄵ',
    ('ㄴ','ㅎ'):'ㄶ',
    ('ㄹ','ㄱ'):'ㄺ',
    ('ㄹ','ㅁ'):'ㄻ',
    ('ㄹ','ㅂ'):'ㄼ',
    ('ㄹ','ㅅ'):'ㄽ',
    ('ㄹ','ㅌ'):'ㄾ',
    ('ㄹ','ㅍ'):'ㄿ',
    ('ㄹ','ㅎ'):'ㅀ',
    ('ㅂ','ㅅ'):'ㅄ'   
}
seq_first = {}
seq_second = {}
seq_third = {}

bat_print_str = ""
bat_now_status = [None, None, None, None, None, None]
mapping = {
    'q':'ㅂ','Q':'ㅃ',
    'w':'ㅈ','W':'ㅉ',
    'e':'ㄷ','E':'ㄸ',
    'r':'ㄱ','R':'ㄲ',
    't':'ㅅ','T':'ㅆ',
    'y':'ㅛ',
    'u':'ㅕ',
    'i':'ㅑ',
    'o':'ㅐ','O':'ㅒ',
    'p':'ㅔ','P':'ㅖ',
    'a':'ㅁ',
    's':'ㄴ',
    'd':'ㅇ',
    'f':'ㄹ',
    'g':'ㅎ',
    'h':'ㅗ',
    'j':'ㅓ',
    'k':'ㅏ',
    'l':'ㅣ',
    'z':'ㅋ',
    'x':'ㅌ',
    'c':'ㅊ',
    'v':'ㅍ',
    'b':'ㅠ',
    'n':'ㅜ',
    'm':'ㅡ',
    '<':'bSpace'
}


def do_combine(hangul_jamo):
    # 0xAC00 + 
    #19 * 21 * 28 = 11172
    jamo_result = [None, None, None]
    jamo_result[0] = hangul_jamo[0]
    if hangul_jamo[2] is not None:
        jamo_result[1] = second_combine_dict[(hangul_jamo[1],hangul_jamo[2])]
    else:
        jamo_result[1] = hangul_jamo[1]
    if hangul_jamo[4] is not None:
        jamo_result[2] = third_combine_dict[(hangul_jamo[3],hangul_jamo[4])]
    else:
        jamo_result[2] = hangul_jamo[3]
    unicode_jamo = 0xAC00 + seq_first[jamo_result[0]] * 21 * 28 + seq_second[jamo_result[1]] * 28 + seq_third[jamo_result[2]];
    return chr(unicode_jamo)

def translate_for_print(now_state,print_state):
    will_be_added = ""
    if print_state[0] == 0:
        will_be_added = ""
    elif print_state[0] == 1:
        will_be_added = bat_now_status[1]
    else:
        will_be_added = do_combine(bat_now_status[1:print_state[0]+1] + [None for _ in range(print_state[0]+1,6)])
    if print_state[1] is not None:
        will_be_added += print_state[1]
    if print_state[0] != 0 and now_state[1] != print_state[0]:
        bat_now_status[1] = bat_now_status[now_state[1]]
    return will_be_added

def mealy(M,x,bat_first = True):
    global bat_print_str
    global bat_now_status
    bat_print_str = ""
    bat_now_status = [None for _ in range(6)]
    Q,Sigma,Pi,Delta,Lambda,q0 = M
    now_state = q0
    next_state = None
    for sym in x:
        Symbol = mapping[sym]    
        #print(Symbol,end=' ')
        if Symbol == 'bSpace':
            if now_state[1] == 0:
                if len(bat_print_str)>0:
                    bat_print_str = bat_print_str[:-1]
            else:
                if now_state[1] == 4:
                    if bat_now_status[3] is None:
                        now_state = (bat_now_status[2],2)
                    else:
                        now_state = (bat_now_status[3],3)
                elif now_state[1] == 1:
                    now_state = (None,0)
                else:
                    temp_var_now_state = now_state[1]
                    now_state = (bat_now_status[temp_var_now_state-1],temp_var_now_state-1)

        elif (now_state,Symbol) in Delta and (now_state,Symbol) in Lambda:
            print_state = Lambda[(now_state,Symbol)]
            next_state = Delta[(now_state,Symbol)]
            bat_print_str = bat_print_str + translate_for_print(now_state,print_state)
            now_state = next_state
            bat_now_status[now_state[1]] = now_state[0]
        else:
            return "No path exists!"
        for i in range(now_state[1]+1,6):
            bat_now_status[i] = None
    if bat_first:
        bat_print_str = bat_print_str + translate_for_print(now_state,(now_state[1],""))
    else:
        if now_state[1] <= 3:
            bat_print_str = bat_print_str + translate_for_print(now_state,(now_state[1],""))
        else:
            bat_print_str = bat_print_str + translate_for_print(now_state,(now_state[1]-1,bat_now_status[now_state[1]]))
    return bat_print_str
    
def make_dfa():
    dfaQ = [None]
    dfaSigma = real_first + ['ㅏ','ㅐ','ㅑ','ㅒ','ㅓ','ㅔ','ㅕ','ㅖ','ㅗ','ㅛ','ㅜ','ㅠ','ㅡ','ㅣ']
    for i in range(127):
        dfaSigma.append(chr(i))
        for j in range(1,6):
            dfaQ.append((chr(i),j))
    dfaDelta = {}
    dfaLambda = {}
    dfaPi = []
    dfaQ.append((None,0))
    for one_char in dfaSigma:
        #0 : Empty, 1: 초성, 2: 중성 1, 3: 중성 2, 4: 종성 1, 5: 종성 2
        for i in range(1,6):
            dfaQ.append((one_char,i))
    for i in range(0,6):
        dfaPi.append((i,None))
        for one_char in dfaSigma:
            dfaPi.append((i,one_char))
    #one_char with state 0(Empty)
    for second_char in dfaSigma:
        if not (second_char in real_first) and not (second_char in real_second):
            dfaDelta[((None,0),second_char)] = (None,0)
            dfaLambda[((None,0),second_char)] = (0,second_char)
            continue
        if second_char in real_first: # if second_char is jaeum
            dfaDelta[((None,0),second_char)] = (second_char,1)
            dfaLambda[((None,0),second_char)] = (0,None) # print_nothing
        else:                         # if second_char is moeum
            dfaDelta[((None,0),second_char)] = (None,0)
            dfaLambda[((None,0),second_char)] = (0,second_char) # print second_char
    #one_char with state 1(초성)
    for first_char in dfaSigma:
        if not (first_char in real_first): continue # if first_char is moeum
        for second_char in dfaSigma:
            if not (second_char in real_first) and not (second_char in real_second):
                dfaDelta[((first_char,1),second_char)] = (None,0)
                dfaLambda[((first_char,1),second_char)] = (1,second_char)
                continue
            if second_char in real_first: # if second_char is jaeum
                dfaDelta[((first_char,1),second_char)] = (second_char,1)
                dfaLambda[((first_char,1),second_char)] = (1,None) # print chosung
            else:                         # if second_char is moeum
                dfaDelta[((first_char,1),second_char)] = (second_char,2)
                dfaLambda[((first_char,1),second_char)] = (0,None) # print nothing
    #one_char with state 2(중성 1)
    for first_char in dfaSigma:
        if (first_char in real_first): continue # if first_char is jaeum
        for second_char in dfaSigma:
            if not (second_char in real_first) and not (second_char in real_second):
                dfaDelta[((first_char,2),second_char)] = (None,0)
                dfaLambda[((first_char,2),second_char)] = (2,second_char)
                continue
            if second_char in real_first: # if second_char is jaeum
                if second_char in real_third:
                    dfaDelta[((first_char,2),second_char)] = (second_char,4)
                    dfaLambda[((first_char,2),second_char)] = (0,None) # print nothing
                else:
                    dfaDelta[((first_char,2),second_char)] = (second_char,1)
                    dfaLambda[((first_char,2),second_char)] = (2,None) # print until first_char
            else:                         # if second_char is moeum
                if (first_char,second_char) in second_combine_dict:
                    dfaDelta[((first_char,2),second_char)] = (second_char,3)
                    dfaLambda[((first_char,2),second_char)] = (0,None) # print nothing
                else:
                    dfaDelta[((first_char,2),second_char)] = (None,0)
                    dfaLambda[((first_char,2),second_char)] = (2,second_char) # print chosung and jungsung, and now second_char
    #one_char with state 3 (중성 2)
    for first_char in dfaSigma:
        if (first_char in real_first): continue # if first_char is jaeum
        for second_char in dfaSigma:
            if not (second_char in real_first) and not (second_char in real_second):
                dfaDelta[((first_char,3),second_char)] = (None,0)
                dfaLambda[((first_char,3),second_char)] = (3,second_char)
                continue
            if second_char in real_first: # if second_char is jaeum
                if second_char in real_third:
                    dfaDelta[((first_char,3),second_char)] = (second_char,4)
                    dfaLambda[((first_char,3),second_char)] = (0,None) # print nothing
                else:
                    dfaDelta[((first_char,3),second_char)] = (second_char,1)
                    dfaLambda[((first_char,3),second_char)] = (3,None) # print until first_char
            else:                         # if second_char is moeum
                dfaDelta[((first_char,3),second_char)] = (None,0)
                dfaLambda[((first_char,3),second_char)] = (3,second_char) # print chosung and jungsung, and now second_char
    #one_char with state 4 (종성 1)
    for first_char in dfaSigma:
        if not (first_char in real_first): continue # if first_char is moeum
        for second_char in dfaSigma:
            if not (second_char in real_first) and not (second_char in real_second):
                dfaDelta[((first_char,4),second_char)] = (None,0)
                dfaLambda[((first_char,4),second_char)] = (4,second_char)
                continue
            if second_char in real_first: # if second_char is jaeum
                if second_char in real_third:
                    if (first_char,second_char) in third_combine_dict: # second_char가 종성일 가능성이 있다
                        dfaDelta[((first_char,4),second_char)] = (second_char,5)
                        dfaLambda[((first_char,4),second_char)] = (0,None) # print nothing
                    else:                                              # first_char는 종성, second_char는 초성이다
                        dfaDelta[((first_char,4),second_char)] = (second_char,1)
                        dfaLambda[((first_char,4),second_char)] = (4,None) # print until first_char
                else:
                    dfaDelta[((first_char,4),second_char)] = (second_char,1)
                    dfaLambda[((first_char,4),second_char)] = (4,None) # print nothing
            else:                         # if second_char is moeum, 이것은 종성이 아니라 다음 글자의 초성이다
                dfaDelta[((first_char,4),second_char)] = (second_char,2)
                dfaLambda[((first_char,4),second_char)] = (3,None) # print before first_char
    #one_char with state 5 (종성 2)
    for first_char in dfaSigma:
        if not (first_char in real_first): continue # if first_char is moeum
        for second_char in dfaSigma:
            if not (second_char in real_first) and not (second_char in real_second):
                dfaDelta[((first_char,5),second_char)] = (None,0)
                dfaLambda[((first_char,5),second_char)] = (5,second_char)
                continue
            if second_char in real_first: # if second_char is jaeum, first_char는 종성 2, second_char는 초성이다.
                dfaDelta[((first_char,5),second_char)] = (second_char,1)
                dfaLambda[((first_char,5),second_char)] = (5,None) # print until first_char
            else:                         # if second_char is moeum, first_char는 종성이 아니라 다음 글자의 초성이다
                dfaDelta[((first_char,5),second_char)] = (second_char,2)
                dfaLambda[((first_char,5),second_char)] = (4,None) # print before first_char
    dfaQ0 = (None,0)
    return (dfaQ,dfaSigma,dfaPi,dfaDelta,dfaLambda,dfaQ0)


def main():
    #mapping
    #print(real_first)
    #print(real_second)
    #print(real_third)
    for i in range(128):
        if chr(i) in mapping:
            continue
        else:
            mapping[chr(i)] = chr(i)
    #mapping[" "] = "_"
    for i in range(len(real_first)):
        seq_first[real_first[i]] = i
    for i in range(len(real_second)):
        seq_second[real_second[i]] = i
    for i in range(len(real_third)):
        seq_third[real_third[i]] = i
    M = make_dfa()
    bat_first = False
    query_str = input("받침우선 방식을 사용하시겠습니까? [Y/N]: ")
    query_str = query_str.rstrip()
    if query_str == "Y" or  query_str == "y":
        bat_first = True
    else:
        bat_first = False
    while True:
        x = input("Input: ").rstrip()
        #for i in range(1,len(x)):
        #    print(mealy(M,x[:i],bat_first))
        print("Output: " + mealy(M,x,bat_first))
    #test: tkfamlsmvdptj
    #test: qkqtekkk
    #make_dfa_second()
    #mealy_second()


main()
