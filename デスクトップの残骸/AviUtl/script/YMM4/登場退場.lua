local function GetValue(from,to,type,mode,toujou,taijou)
	local rate = 1
	if toujou == 1 then
		rate = math.min(math.max(math.min(obj.time / obj.track0,1),0),rate)
	end
	if taijou == 1 then
		rate = math.min(math.max(math.min((obj.totaltime - obj.time) / obj.track0,1),0),rate)
	end
	local ease = require("YMM4/ease")
	return from + (to - from)*ease[type..mode](rate)
end
return
{
	GetValue = GetValue,
}