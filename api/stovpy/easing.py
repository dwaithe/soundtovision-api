import math
class EasingFunctions:
    def __init__(self):
        self.c1 = 1.70158;
        self.c2 = self.c1 * 1.525;
        self.c3 = self.c1 + 1;
        self.c4 = (2 * math.pi) / 3;
        self.c5 = (2 *math.pi) / 4.5;
        methods = {}
        methods['linear'] = self.linear
        methods['none'] = self.none
        methods['step'] = self.step
        #methods['steps'] = self.steps
        methods['easeInSine'] = self.easeInSine
        methods['easeOutSine'] = self.easeOutSine
        methods['easeInOutSine'] = self.easeInOutSine
        methods['easeInQuad'] = self.easeInQuad
        methods['easeOutQuad'] = self.easeOutQuad
        methods['easeInOutQuad'] = self.easeInOutQuad
        methods['easeInCubic'] = self.easeInCubic
        methods['easeOutCubic'] = self.easeOutCubic
        methods['easeInOutCubic'] = self.easeInOutCubic
        methods['easeInQuart'] = self.easeInQuart
        methods['easeOutQuart'] = self.easeOutQuart
        methods['easeInOutQuart'] = self.easeInOutQuart
        methods['easeInQuint'] = self.easeInQuint
        methods['easeOutQuint'] = self.easeOutQuint
        methods['easeInOutQuint'] = self.easeInOutQuint
        methods['easeInExpo'] = self.easeInExpo
        methods['easeOutExpo'] = self.easeOutExpo
        methods['easeInOutExpo'] = self.easeInOutExpo
        methods['easeInCirc'] = self.easeInCirc
        methods['easeOutCirc'] = self.easeOutCirc
        methods['easeInOutCirc'] = self.easeInOutCirc
        methods['easeInBack'] = self.easeInBack
        methods['easeOutBack'] = self.easeOutBack
        methods['easeInOutBack'] = self.easeInOutBack
        methods['easeInElastic'] = self.easeInElastic
        methods['easeOutElastic'] = self.easeOutElastic
        methods['easeInOutElastic'] = self.easeInOutElastic
        methods['easeInBounce'] = self.easeInBounce
        methods['easeOutBounce'] = self.easeOutBounce
        methods['easeInOutBounce'] = self.easeInOutBounce
        self.methods = methods
    def linear(self,x):
        return x
    def none(self,x):
        return 0
    def step(self,x):
        return 1 if x > 0.5 else 0
    def easeOutBounce(self,x):
        if t < 4 / 11:
            return 121 * t * t / 16
        elif t < 8 / 11:
            return (363 / 40.0 * t * t) - (99 / 10.0 * t) + 17 / 5.0
        elif t < 9 / 10:
            return (4356 / 361.0 * t * t) - (35442 / 1805.0 * t) + 16061 / 1805.0
        return (54 / 5.0 * t * t) - (513 / 25.0 * t) + 268 / 25.0

    def easeInQuad(self,x):
        return x * x;
    def easeOutQuad(self,x):
        return 1 - (1 - x) * (1 - x);
    def easeInOutQuad(self,x):
        return 2 * x * x  if x < 0.5  else 1 -math.pow(-2 * x + 2, 2) / 2;
    def easeInCubic(self,x):
        return x * x * x;
    def easeOutCubic(self,x):
        return 1 -math.pow(1 - x, 3);
    def easeInOutCubic(self,x):
        return 4 * x * x * x if x < 0.5 else 1 -math.pow(-2 * x + 2, 3) / 2;
    def easeInQuart(self,x):
        return x * x * x * x;
    def easeOutQuart(self,x):
        return 1 -math.pow(1 - x, 4);
    def easeInOutQuart(self,x):
        return 8 * x * x * x * x if x < 0.5 else 1 -math.pow(-2 * x + 2, 4) / 2;
    def easeInQuint(self,x):
        return x * x * x * x * x;
    def easeOutQuint(self,x):
        return 1 -math.pow(1 - x, 5);
    def easeInOutQuint(self,x):
        return 16 * x * x * x * x * x if x < 0.5 else 1 -math.pow(-2 * x + 2, 5) / 2;
    def easeInSine(self,x):
        return 1 -math.cos((x *math.pi) / 2);
    def easeOutSine(self,x):
        return math.sin((x *math.pi) / 2);
    def easeInOutSine(self,x):
        return -(math.cos(math.pi * x) - 1) / 2;
    def easeInExpo(self,x):
        return 0 if x == 0 else math.pow(2, 10 * x - 10);
    def easeOutExpo(self,x):
        return 1 if x == 1 else 1 -math.pow(2, -10 * x);
    def easeInOutExpo(self,x):
        
            if(x == 0):
                return 0
            elif(x == 1):
                return 0
            elif(x < 0.5):
                return math.pow(2, 20 * x - 10) / 2
            else:
                return (2 -math.pow(2, -20 * x + 10)) / 2;
    def easeInCirc(self,x):
        return 1 -math.sqrt(1 -math.pow(x, 2));

    def easeOutCirc(self,x):
        return math.sqrt(1 -math.pow(x - 1, 2));
    def easeInOutCirc(self,x):
        if( x < 0.5):
            return (1 - math.sqrt(1 - math.pow(2 * x, 2))) / 2
        else:
            return (math.sqrt(1 - math.pow(-2 * x + 2, 2)) + 1) / 2;
    def easeInBack(self,x):
        
        return self.c3 * x * x * x - self.c1 * x * x;

    def easeOutBack(self,x):
        return 1 + self.c3 * math.pow(x - 1, 3) + self.c1 * math.pow(x - 1, 2);
    def easeInOutBack(self,x):
        if( x < 0.5):
            return (math.pow(2 * x, 2) * ((self.c2 + 1) * 2 * x - self.c2)) / 2
        else:
            return (math.pow(2 * x - 2, 2) * ((self.c2 + 1) * (x * 2 - 2) + self.c2) + 2) / 2;
    def easeInElastic(self,x):
        if(x == 0):
            return 0
        elif(x == 1):
            return 1
        else:
            return -math.pow(2, 10 * x - 10) * math.sin((x * 10 - 10.75) * self.c4);
    def easeOutElastic(self,x):
        if(x == 0):
            return 0
        elif(x == 1):
            return 1
        else:
            return math.pow(2, -10 * x) * math.sin((x * 10 - 0.75) * self.c4) + 1;
    def easeInOutElastic(self,x):
        if(x == 0):
            return 0
        elif(x == 1):
            return 1
        elif (x < 0.5):
            return -(math.pow(2, 20 * x - 10) * math.sin((20 * x - 11.125) * self.c5)) / 2
        else:
            return (math.pow(2, -20 * x + 10) * math.sin((20 * x - 11.125) * self.c5)) / 2 + 1;
    def easeInBounce(self,x):
        return 1 - self.easeOutBounce(1 - x);

    def easeInOutBounce(self,x):
        if(x < 0.5):
            return (1 - self.easeOutBounce(1 - 2 * x)) / 2
        else:
            return (1 + self.easeOutBounce(2 * x - 1)) / 2;