local function LoadRoundedRect(obj, width, height, thickness, color, round)
	local roundWidth  = math.min(round*2, width)
	local roundHeight = math.min(round*2, height)
	local roundSize = math.max(roundWidth, roundHeight)
	local roundAspect = (roundWidth - roundHeight) / math.max(roundWidth, roundHeight)

	obj.setoption("drawtarget", "tempbuffer", width, height)

	obj.load("figure", "�~", color, roundSize, thickness)
	obj.drawpoly(-width/2-1,-height/2-1,0, -width/2+roundWidth/2,-height/2-1,0, -width/2+roundWidth/2,-height/2+roundHeight/2,0, -width/2-1,-height/2+roundHeight/2, 0,        0,0, roundSize/2,0, roundSize/2,roundSize/2, 0,roundSize/2)
	obj.drawpoly( width/2+1, height/2+1,0,  width/2-roundWidth/2, height/2+1,0,  width/2-roundWidth/2, height/2-roundHeight/2,0,  width/2+1, height/2-roundHeight/2, 0,        0,0, roundSize/2,0, roundSize/2,roundSize/2, 0,roundSize/2)
	obj.drawpoly( width/2+1,-height/2-1,0,  width/2-roundWidth/2,-height/2-1,0,  width/2-roundWidth/2,-height/2+roundHeight/2,0,  width/2+1,-height/2+roundHeight/2, 0,        0,0, roundSize/2,0, roundSize/2,roundSize/2, 0,roundSize/2)
	obj.drawpoly(-width/2-1, height/2+1,0, -width/2+roundWidth/2, height/2+1,0, -width/2+roundWidth/2, height/2-roundHeight/2,0, -width/2-1, height/2-roundHeight/2, 0,        0,0, roundSize/2,0, roundSize/2,roundSize/2, 0,roundSize/2)

	obj.load("figure", "�l�p�`", color, 1,1)

	local hRate = math.min(1,roundHeight/roundWidth)
	obj.drawpoly(-width/2+roundWidth/2,-height/2,0, width/2-roundWidth/2,-height/2,0, width/2-roundWidth/2,-height/2+thickness*hRate,0, -width/2+roundWidth/2,-height/2+thickness*hRate,0)
	obj.drawpoly(-width/2+roundWidth/2, height/2,0, width/2-roundWidth/2, height/2,0, width/2-roundWidth/2, height/2-thickness*hRate,0, -width/2+roundWidth/2, height/2-thickness*hRate,0)

	local vRate = math.min(1,roundWidth/roundHeight)
	obj.drawpoly(-width/2,-height/2+roundHeight/2,0, -width/2+thickness*vRate,-height/2+roundHeight/2,0, -width/2+thickness*vRate, height/2-roundHeight/2,0, -width/2, height/2-roundHeight/2,0)
	obj.drawpoly( width/2,-height/2+roundHeight/2,0,  width/2-thickness*vRate,-height/2+roundHeight/2,0,  width/2-thickness*vRate, height/2-roundHeight/2,0,  width/2, height/2-roundHeight/2,0)

	obj.load("tempbuffer")
end

-- �J�X�^���I�u�W�F�N�g�͖��O�Ŏw�肪�ł����f�t�H���g���ȊO�ł̓����ۏ؂ł��Ȃ����߁A�A�j���[�V�������ʂōĎ����B
-- �J�X�^���I�u�W�F�N�g�u��^�v���珈�������؂肵����ňꕔ�̏��������ς��Ă��܂��B
local function LoadFan(obj, l, r, rotate, thickness, color)
	obj.load("figure", "�~", color, l * 2, thickness)
	obj.effect("�΂߃N���b�s���O", "�p�x", r)
	obj.effect("�~���[", "���ڒ���", -l)
	obj.rz = obj.rz + 90+r * rotate / 100
end

local function LoadWedge(obj, size, rate, thickness, color)
	obj.load("figure", "�O�p�`", color, size, thickness)
	obj.effect("�}�X�N", "type", 3, "�c����", -rate * 100, "�}�X�N�̔��]", 1, "�T�C�Y", size, "Y", size * rate / 4 + 1)
end

local function LoadArrow(obj, size, rate, length, stroke, type, color)
	local width  = size
	local height = size + length
	obj.setoption("drawtarget", "tempbuffer", width, height)

	obj.load("figure", "�O�p�`", color, size, 4000)
	obj.effect("�}�X�N", "type", 3, "�c����", -rate * 100, "�}�X�N�̔��]", 1, "�T�C�Y", size, "Y", size * rate / 4 + 1)
	obj.draw(0,-height/2+size/2)

	if type == 0 then
		obj.load("figure", "�O�p�`", color, length, 4000)
	elseif type == 1 or type == 2 then
		obj.load("figure", "�l�p�`", color, length, 4000)
	end
	obj.drawpoly(stroke/2,-height/2+size/2+length,0, -stroke/2,-height/2+size/2+length,0, -stroke/2,-height/2+size/2,0, stroke/2,-height/2+size/2,0,     0,0, length,0, length,length*3/4, 0,length*3/4)
	if type == 2 then
		obj.load("figure", "�O�p�`", color, size, 4000)
		obj.effect("�}�X�N", "type", 3, "�c����", -rate * 100, "�}�X�N�̔��]", 1, "�T�C�Y", size, "Y", size * rate / 4 + 1)
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