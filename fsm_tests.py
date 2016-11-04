import unittest
from fsm import FSM

class TestMatching(unittest.TestCase):
    def test_constuctor(self):
        f = FSM()
        assert(type(f) == FSM)
        assert(f.currentState is None)
        assert(len(f.acceptStates) == 0)
        assert(f.startState is None)
        assert(len(f.states) == 0)
        
    def test_setstartstate(self):
        # adding state then declaring startstate
        f = FSM()
        f.addstate('freshman')
        f.addstate('sophmore')
        f.addstate('junior')
        f.addstate('senior')
        f.setstartstate('freshman')
        assert(f.startState.state == 'freshman')
        assert(f.startState.state in f.states)

        # adding and declaring startstate at once
        f = FSM()
        f.setstartstate('freshman')
        assert(f.startState.state == 'freshman')
        assert(f.startState.state in f.states)
        
    def test_setacceptstate(self):
        f = FSM()
        f.addstate('freshman')
        f.setacceptstate('freshman')
        assert('freshman' in f.acceptStates)

        # labeling non-existant state as an accept state
        f = FSM()
        f.addstate('sophmore')
        self.assertRaises(ValueError,f.setacceptstate,'freshman')
        
    def test_addstate(self):
        a = FSM()
        a.addstate('q1')
        a.addstate('q2')
        a.addstate('q3')
        a.addstate('q4')
        a.addstate('q5')
        a.addstate('q6')
        assert(len(a.states) == 6)

    
    def test_accepts_basic(self):
        a = FSM()
        a.setstartstate('q1')
        a.addstate('q2')
        a.setacceptstate('q2')
        a.addtransition('q1','q2','1')
        a.addtransition('q2','q1','0')
        
        self.assertTrue(a.accepts('1')) # True
        self.assertFalse(a.accepts('10')) # False
        self.assertTrue(a.accepts('101')) # True
        self.assertFalse(a.accepts('1010')) # False
        self.assertFalse(a.accepts('1010101110001110101')) # This depends on how you handle invalid letters
        self.assertFalse(a.accepts('10101010101010101010')) # False
        
        a.addstate('q3')
        a.addtransition('q2','q3','1')
        a.addtransition('q3','q1','1')
        
        self.assertFalse(a.accepts('11')) # False
        self.assertTrue(a.accepts('1111')) # True
        self.assertFalse(a.accepts('10101111011')) # False
        
        a.addtransition('q3','q2','1')
        
        self.assertTrue(a.accepts('111')) # True - this fails bc this is deterministic
        self.assertFalse(a.accepts('')) # False
        self.assertFalse(a.accepts('14')) # # This depends on how you handle invalid letters

        self.assertTrue(a.accepts('1')) # True

    def test_accepts_basic_2(self):
        a = FSM()
        a.setstartstate('q1')
        a.addstate('q2')
        a.addstate('q3')
        a.addstate('q4')
        a.addstate('q5')
        a.addstate('q6')

        a.setacceptstate('q2')
        a.setacceptstate('q5')
        a.addtransition('q1','q2','1')
        a.addtransition('q2','q1','0')
        a.addtransition('q1','q1','0')
        a.addtransition('q2','q3','0')
        a.addtransition('q3','q4','0')
        a.addtransition('q4','q5','0')
        a.addtransition('q5','q6','0')
        a.addtransition('q6','q3','1')

        
        self.assertFalse(a.accepts('0010')) # False
        self.assertFalse(a.accepts('10')) # False
        self.assertFalse(a.accepts('100')) # False
        self.assertTrue(a.accepts('1000')) # True
        self.assertTrue(a.accepts('0101')) # True
        self.assertTrue(a.accepts('100001')) # True
        a.addtransition('q3','q2','0')
        self.assertTrue(a.accepts('1000010')) # True
        self.assertTrue(a.accepts('101000001000')) # True
        self.assertFalse(a.accepts('1010000011')) # This depends on the case of invalid alphabets

    def test_accepts_basic_3(self):
        f = FSM()
        f.addstate('freshman')
        f.addstate('sophmore')
        f.addstate('junior')
        f.addstate('senior')
        f.setstartstate('freshman')
        f.addtransition('freshman','freshman','F')
        f.addtransition('sophmore','sophmore','F')
        f.addtransition('junior','junior','F')
        f.addtransition('senior','senior','F')
        f.addtransition('freshman','sophmore','A')
        f.addtransition('sophmore','junior','A')
        f.addtransition('junior','senior','A')
        f.addtransition('senior','freshman','F')
        f.addtransition('junior','freshman','F')
        f.addtransition('sophmore','freshman','F')
        f.setacceptstate('senior')

        self.assertTrue(f.accepts('AAA')) # True
        self.assertTrue(f.accepts('AAAF')) # True
        self.assertTrue(f.accepts('AAAFAAA')) # True
        self.assertTrue(f.accepts('FAFAAFAAA')) # True
        self.assertTrue(f.accepts('FAFAAFA')) # True
        self.assertTrue(f.accepts('AFAA')) 

        self.assertFalse(f.accepts('AA')) 
        self.assertFalse(f.accepts('FAFF'))
        self.assertFalse(f.accepts('AAAA')) 
        self.assertFalse(f.accepts('AFFFFF')) 
        self.assertFalse(f.accepts('AFAAFAFA'))

    def test_accepts_invalidInput(self):
        f = FSM()
        f.addstate("python")
        f.addstate("java")
        f.addstate("c")
        f.addstate("c++")
        f.addstate("scheme")
        f.setstartstate("java")

        # transitions longer than length 1
        f.addtransition("java","scheme","1729")
        f.addtransition("scheme","python","2050")
        f.addtransition("python","c++","4095")
        f.addtransition("c++","c","4095")
        
        self.assertFalse(f.accepts("1729"))
        self.assertFalse(f.accepts("17292050"))
        self.assertFalse(f.accepts("172920504095"))
        self.assertFalse(f.accepts("1729205040954095"))

        # invalid paramter type
        self.assertRaises(TypeError,f.accepts,1729205040954095)


    def test_accepts_noStates(self):
        f = FSM()
        # testing accepts without given a startstate
        self.assertRaises(ValueError,f.accepts,'10121')

        # given non-existent states
        f.setstartstate("pie")
        self.assertRaises(KeyError,f.addtransition,'fail','this','1')
        self.assertFalse(f.accepts("thereisnothing"))
        
    def test_accepts_noTransitions(self):
        f = FSM()
        f.addstate('a')
        f.addstate('b')
        f.addstate('c')
        f.addstate('d')
        f.setstartstate('a')
        self.assertFalse(f.accepts("thereisnopath"))
        f.addtransition('d', 'b', '0')
        f.addtransition('d', 'b', '1')
        f.addtransition('d', 'c', '0')
        f.addtransition('d', 'c', '1')
        self.assertFalse(f.accepts("thereisnopath"))
        
    def test_all_ones(self):
        M = FSM()
        M.addstate('allones')
        M.addstate('fail')
        M.addtransition('allones', 'allones', '1')
        M.addtransition('allones', 'fail', '0')
        M.addtransition('fail', 'fail', '0')
        M.addtransition('fail', 'fail', '1')
        M.setstartstate('allones')
        M.setacceptstate('allones')
        assert(M.accepts(''))
        assert(M.accepts('1'))
        assert(M.accepts('11111111'))
        assert(not M.accepts('11111110'))
        assert(not M.accepts('0')) 

    def test_odd_number_of_zeros(self):
        M = FSM()
        M.addstate('oddzeros')
        M.addstate('evenzeros')
        M.addtransition('evenzeros', 'evenzeros', '1')
        M.addtransition('evenzeros', 'oddzeros', '0')
        M.addtransition('oddzeros', 'oddzeros', '1')
        M.addtransition('oddzeros', 'evenzeros', '0')
        M.setstartstate('evenzeros')
        M.setacceptstate('oddzeros')
        assert(M.accepts('0'))
        assert(M.accepts('10010'))
        assert(M.accepts('11101010111'))
        assert(not M.accepts('00'))
        assert(not M.accepts('0000'))    
        assert(not M.accepts('1110101010111111'))

    def test_new_fsm(self):
        M = FSM()
        M.addstate('open')
        M.addstate('closed')
        M.addtransition('open', 'closed', 'a')
        M.addtransition('closed', 'open', 'b')
        M.setstartstate('closed')
        assert(M.accepts('a') == False)
        M.setacceptstate('open')
        assert(M.accepts('a') == False)
        assert(M.accepts('b') == True)
        assert(M.accepts('bab') == True)
        assert(M.accepts('ba') == False)

    def test_multiple_accept_states(self):
        M =FSM()
        for i in range(5):
            M.addstate(str(i))
        for i in range(4):
            M.addtransition(str(i), str(i+1), 'a')
        M.setstartstate('0')
        assert(M.accepts('aaa') == False)
        M.setacceptstate('4')
        assert(M.accepts('aaa') == False)
        assert(M.accepts('aaaa') == True)
        M.setacceptstate('3')
        assert(M.accepts('aaa') == True)
        assert(M.accepts('aaaa') == True)

    def test_highly_connected(self):
        m = FSM()
        m.addstate('a')
        m.addstate('b')
        m.addstate('c')
        m.addstate('d')
        m.addtransition('a', 'b', '0')
        m.addtransition('a', 'b', '1')
        m.addtransition('a', 'c', '0')
        m.addtransition('a', 'c', '1')
        m.addtransition('a', 'd', '0')
        m.addtransition('a', 'd', '1')
        m.addtransition('b', 'a', '0')
        m.addtransition('b', 'a', '1')
        m.addtransition('b', 'c', '0')
        m.addtransition('b', 'c', '1')
        m.addtransition('b', 'd', '0')
        m.addtransition('b', 'd', '1')
        m.addtransition('c', 'a', '0')
        m.addtransition('c', 'a', '1')
        m.addtransition('c', 'b', '0')
        m.addtransition('c', 'b', '1')
        m.addtransition('c', 'd', '0')
        m.addtransition('c', 'd', '1')
        m.addtransition('d', 'a', '0')
        m.addtransition('d', 'a', '1')
        m.addtransition('d', 'b', '0')
        m.addtransition('d', 'b', '1')
        m.addtransition('d', 'c', '0')
        m.addtransition('d', 'c', '1')
        m.setstartstate('a')
        assert(m.accepts('00000') == False)
        m.setacceptstate('b')
        assert(m.accepts('00000') == True)
        assert(m.accepts('01010101010') == True)
        assert(m.accepts('010101010120') == False)
        assert(m.accepts('010101010000000000000000000000000011100010') == True)

    
unittest.main()
        
