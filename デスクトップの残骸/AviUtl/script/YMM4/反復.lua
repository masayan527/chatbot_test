local function GetValue(from,to,type,mode,centering)
	local span = obj.track0
	local time = obj.time;
	if( centering==1 and mode == "InOut") then
		time = time + span / 4
	end

	local halfSpan = span /2
	local spanTime = time % span
	local rate = 0
	if (spanTime < halfSpan) then
		rate = spanTime / halfSpan
	else
		rate = 1 - (spanTime % halfSpan) / halfSpan
	end

	local ease = require("YMM4/ease")
	local offset = 0
	if(centering == 1) then
		offset = - (to - from) / 2
	end

	return offset + from + (to - from) * ease[type..mode](rate)
end
return
{
	GetValue = GetValue,
}