# ScratchABit - interactive disassembler
#
# Copyright (c) 2015 Paul Sokolovsky
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import logging as log

from scratchabit import engine
import idaapi


SEGATTR_PERM = 1


def GetReg(ea, reg):
    assert reg == "T"
    if engine.ADDRESS_SPACE.get_flags(ea, engine.AddressSpace.ALT_CODE):
        return 1
    return 0


def GetSegmentAttr(ea, attr):
    assert attr == SEGATTR_PERM
    off, area = engine.ADDRESS_SPACE.addr2area(addr)
    props = engine.area_props(area)
    ret = 0
    if "R" in props:
        ret |= idaapi.SEGPERM_READ
    if "W" in props:
        ret |= idaapi.SEGPERM_WRITE
    if "X" in props:
        ret |= idaapi.SEGPERM_EXEC


# Make filler
def MakeAlign(ea, cnt, align):
    engine.ADDRESS_SPACE.make_filler(ea, cnt)


def SetReg(ea, reg, val):
    assert reg == "T"
    try:
        if val:
            engine.ADDRESS_SPACE.update_flags(ea, 0xff, engine.AddressSpace.ALT_CODE)
        else:
            engine.ADDRESS_SPACE.update_flags(ea, ~engine.AddressSpace.ALT_CODE, 0)
    except engine.InvalidAddrException:
        log.exception("")

def SetRegEx(ea, reg, val, tag):
    if(engine.ADDRESS_SPACE.is_valid_addr(ea)):
        SetReg(ea,reg,val)
        engine.add_entrypoint(ea, False)
        engine.analyze()

def MakeComm(ea, comment):
    if(engine.ADDRESS_SPACE.is_valid_addr(ea)):
        engine.ADDRESS_SPACE.set_comment(ea, comment)

def MakeFunction(ea, color):
    if(engine.ADDRESS_SPACE.is_valid_addr(ea)):
        engine.add_entrypoint(ea, True)
    # TODO: use the color

def MakeNameEx(ea, funcname, flags):
    if(engine.ADDRESS_SPACE.is_valid_addr(ea)):
        engine.ADDRESS_SPACE.make_label(funcname, ea)
    # TODO: use the flags
