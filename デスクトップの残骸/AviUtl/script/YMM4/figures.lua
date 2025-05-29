local function LoadRoundedRect(obj, width, height, thickness, color, round)
	local roundWidth  = math.min(round*2, width)
	local roundHeight = math.min(round*2, height)
	local roundSize = math.max(roundWidth, roundHeight)
	local roundAspect = (roundWidth - roundHeight) / math.max(roundWidth, roundHeight)

	obj.setoption("drawtarget", "tempbuffer", width, height)

	obj.load("figure", "円", color, roundSize, thickness)
	obj.drawpoly(-width/2-1,-height/2-1,0, -width/2+roundWidth/2,-height/2-1,0, -width/2+roundWidth/2,-height/2+roundHeight/2,0, -width/2-1,-height/2+roundHeight/2, 0,        0,0, roundSize/2,0, roundSize/2,roundSize/2, 0,roundSize/2)
	obj.drawpoly( width/2+1, height/2+1,0,  width/2-roundWidth/2, height/2+1,0,  width/2-roundWidth/2, height/2-roundHeight/2,0,  width/2+1, height/2-roundHeight/2, 0,        0,0, roundSize/2,0, roundSize/2,roundSize/2, 0,roundSize/2)
	obj.drawpoly( width/2+1,-height/2-1,0,  width/2-roundWidth/2,-height/2-1,0,  width/2-roundWidth/2,-height/2+roundHeight/2,0,  width/2+1,-height/2+roundHeight/2, 0,        0,0, roundSize/2,0, roundSize/2,roundSize/2, 0,roundSize/2)
	obj.drawpoly(-width/2-1, height/2+1,0, -width/2+roundWidth/2, height/2+1,0, -width/2+roundWidth/2, height/2-roundHeight/2,0, -width/2-1, height/2-roundHeight/2, 0,        0,0, roundSize/2,0, roundSize/2,roundSize/2, 0,roundSize/2)

	obj.load("figure", "四角形", color, 1,1)

	local hRate = math.min(1,roundHeight/roundWidth)
	obj.drawpoly(-width/2+roundWidth/2,-height/2,0, width/2-roundWidth/2,-height/2,0, width/2-roundWidth/2,-height/2+thickness*hRate,0, -width/2+roundWidth/2,-height/2+thickness*hRate,0)
	obj.drawpoly(-width/2+roundWidth/2, height/2,0, width/2-roundWidth/2, height/2,0, width/2-roundWidth/2, height/2-thickness*hRate,0, -width/2+roundWidth/2, height/2-thickness*hRate,0)

	local vRate = math.min(1,roundWidth/roundHeight)
	obj.drawpoly(-width/2,-height/2+roundHeight/2,0, -width/2+thickness*vRate,-height/2+roundHeight/2,0, -width/2+thickness*vRate, height/2-roundHeight/2,0, -width/2, height/2-roundHeight/2,0)
	obj.drawpoly( width/2,-height/2+roundHeight/2,0,  width/2-thickness*vRate,-height/2+roundHeight/2,0,  width/2-thickness*vRate, height/2-roundHeight/2,0,  width/2, height/2-roundHeight/2,0)

	obj.load("tempbuffer")
end

-- カスタムオブジェクトは名前で指定ができずデフォルト環境以外での動作を保証できないため、アニメーション効果で再実装。
-- カスタムオブジェクト「扇型」から処理をお借りした上で一部の処理を改変しています。
local function LoadFan(obj, l, r, rotate, thickness, color)
	obj.load("figure", "円", color, l * 2, thickness)
	obj.effect("斜めクリッピング", "角度", r)
	obj.effect("ミラー", "境目調整", -l)
	obj.rz = obj.rz + 90+r * rotate / 100
end

local function LoadWedge(obj, size, rate, thickness, color)
	obj.load("figure", "三角形", color, size, thickness)
	obj.effect("マスク", "type", 3, "縦横比", -rate * 100, "マスクの反転", 1, "サイズ", size, "Y", size * rate / 4 + 1)
end

local function LoadArrow(obj, size, rate, length, stroke, type, color)
	local width  = size
	local height = size + length
	obj.setoption("drawtarget", "tempbuffer", width, height)

	obj.load("figure", "三角形", color, size, 4000)
	obj.effect("マスク", "type", 3, "縦横比", -rate * 100, "マスクの反転", 1, "サイズ", size, "Y", size * rate / 4 + 1)
	obj.draw(0,-height/2+size/2)

	if type == 0 then
		obj.load("figure", "三角形", color, length, 4000)
	elseif type == 1 or type == 2 then
		obj.load("figure", "四角形", color, length, 4000)
	end
	obj.drawpoly(stroke/2,-height/2+size/2+length,0, -stroke/2,-height/2+size/2+length,0, -stroke/2,-height/2+size/2,0, stroke/2,-height/2+size/2,0,     0,0, length,0, length,length*3/4, 0,length*3/4)
	if type == 2 then
		obj.load("figure", "三角形", color, size, 4000)
		obj.effect("マスク", "type", 3, "縦横比", -rate * 100, "マスクの反転", 1, "サイズ", size, "Y", size * rate / 4 + 1)
		obj.draw(0,-height/2+size/2+length,0, 1,1, 0,0,180)
	end
	obj.load("tempbuffer")
	obj.cy = -(length)/2
end

return
{
	LoadRoundedRect = LoadRoundedRect,
	LoadFan = LoadFan,
	LoadWedge = LoadWedge,
	LoadArrow = LoadArrow,
}