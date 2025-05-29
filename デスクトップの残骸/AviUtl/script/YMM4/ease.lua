local function In(func,t)
	if t<0 then t = 0 end
	if t>1 then t = 1 end
	return func(t)
end

local function Out(func,t)
	if t<0 then t = 0 end
	if t>1 then t = 1 end
	return 1 - func(1-t)
end

local function InOut(func,t)
	if t<0 then t = 0 end
	if t>1 then t = 1 end
	if t < 0.5 then
		return func(t*2)/2
	else
		return 1 - func(2-2*t)/2
	end
end


local function linear(t)
	return t;
end

local function quad(t)
	return math.pow(t,2)
end

local function cubic(t)
	return math.pow(t,3)
end

local function quart(t)
	return math.pow(t,4)
end

local function quint(t)
	return math.pow(t,5)
end

local function sine(t)
	return 1 - math.cos(math.pi/2*t)
end

local function circ(t)
	return 1 - math.sqrt(math.max(0,1-math.pow(t,2)))
end

local function expo(t)
	return math.pow(2,-(1-t)*10)
end

local function back(t)
	return math.pow(t,2)*(2.70158 *t-1.70158)
end

local function elastic(t)
	return 56 * math.pow(t, 5) - 105 * math.pow(t, 4) + 60 * math.pow(t, 3) - 10 * math.pow(t, 2)
end

local function bounce(t)
	local pow2 = 0;
	local bounce = 4;

	while true do
		bounce = bounce - 1
		pow2 = math.pow(2, bounce)
		if t >= (pow2 - 1) / 11 then
			break
		end
	end
	return 1 / math.pow(4, 3 - bounce) - 7.5625 * math.pow((pow2 * 3 - 2) / 22 - t, 2)
end


return
{
	LinearIn	= function(t) return In(linear,t) end,
	LinearOut	= function(t) return Out(linear,t) end,
	LinearInOut	= function(t) return InOut(linear,t) end,
	
	SineIn		= function(t) return In( sine ,t) end,
	SineOut		= function(t) return Out( sine ,t) end,
	SineInOut	= function(t) return InOut( sine ,t) end,

	QuadIn		= function(t) return In(quad,t) end,
	QuadOut		= function(t) return Out(quad,t) end,
	QuadInOut	= function(t) return InOut(quad,t) end,

	CubicIn		= function(t) return In( cubic ,t) end,
	CubicOut	= function(t) return Out( cubic ,t) end,
	CubicInOut	= function(t) return InOut( cubic ,t) end,

	QuartIn		= function(t) return In( quart ,t) end,
	QuartOut	= function(t) return Out( quart ,t) end,
	QuartInOut	= function(t) return InOut( quart ,t) end,

	QuintIn		= function(t) return In( quint ,t) end,
	QuintOut	= function(t) return Out( quint ,t) end,
	QuintInOut	= function(t) return InOut( quint ,t) end,

	CircIn		= function(t) return In( circ ,t) end,
	CircOut		= function(t) return Out( circ ,t) end,
	CircInOut	= function(t) return InOut( circ ,t) end,

	ExpoIn		= function(t) return In( expo ,t) end,
	ExpoOut		= function(t) return Out( expo ,t) end,
	ExpoInOut	= function(t) return InOut( expo ,t) end,

	BackIn		= function(t) return In( back ,t) end,
	BackOut		= function(t) return Out( back ,t) end,
	BackInOut	= function(t) return InOut( back ,t) end,

	ElasticIn	= function(t) return In( elastic ,t) end,
	ElasticOut	= function(t) return Out( elastic ,t) end,
	ElasticInOut= function(t) return InOut( elastic ,t) end,

	BounceIn	= function(t) return In( bounce ,t) end,
	BounceOut	= function(t) return Out( bounce ,t) end,
	BounceInOut	= function(t) return InOut( bounce ,t) end,
}