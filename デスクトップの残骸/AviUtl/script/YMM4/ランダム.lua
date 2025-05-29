function GetRandomValue(id)
	if (obj.track0 == 0) then
		return obj.rand(0,1000,id) / 1000
	end
	local t = obj.time/obj.track0
	local p = math.floor(t)
	t = t-p

	local a = obj.rand(0,1000,id,p+0) / 1000
	local b = obj.rand(0,1000,id,p+1) / 1000
	local c = obj.rand(0,1000,id,p+2) / 1000
	local d = obj.rand(0,1000,id,p+3) / 1000

	return obj.interpolation(t,a,b,c,d)
end
return
{
	GetRandomValue = GetRandomValue,
}