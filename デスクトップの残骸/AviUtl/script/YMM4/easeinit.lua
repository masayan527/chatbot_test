ease = require("ease")

local res = obj.getpoint("index")
local index = math.floor(res)
rate = res % 1
	
from = obj.getpoint(index)
local to = obj.getpoint(index+1)

delta = to - from

function GetValue(func)
	return from + delta * func(rate)
end

return false