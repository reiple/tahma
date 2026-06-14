from __future__ import annotations

from .models import Player
from .world import World

DIRECTIONS = {
    "북": "북", "북쪽": "북", "north": "북", "n": "북",
    "남": "남", "남쪽": "남", "south": "남", "s": "남",
    "동": "동", "동쪽": "동", "east": "동", "e": "동",
    "서": "서", "서쪽": "서", "west": "서", "w": "서",
}

HELP_TEXT = """사용 가능한 명령어
  보기, 주변, look       현재 장소를 살핍니다.
  북/남/동/서            해당 방향으로 이동합니다.
  소지품, inventory      가진 물건을 봅니다.
  줍기 <물건>            장소의 물건을 줍습니다.
  버리기 <물건>          가진 물건을 내려놓습니다.
  상태, status           체력과 경험치를 확인합니다.
  휴식, rest             잠시 쉬며 체력을 회복합니다.
  공격 <대상>, attack    같은 장소의 적을 공격합니다.
  말 <내용>              같은 서버의 접속자에게 말합니다.
  인코딩 <utf-8|cp949|euc-kr>  현재 접속의 출력 인코딩을 바꿉니다.
  종료, quit             저장 후 접속을 끝냅니다."""


class CommandResult:
    def __init__(self, message: str, should_quit: bool = False, broadcast: str | None = None) -> None:
        self.message = message
        self.should_quit = should_quit
        self.broadcast = broadcast


def execute_command(raw_command: str, player: Player, world: World) -> CommandResult:
    command = raw_command.strip()
    if not command:
        return CommandResult("")

    verb, _, rest = command.partition(" ")
    verb_lower = verb.lower()

    if verb_lower in {"도움말", "명령어", "help", "h", "?"}:
        return CommandResult(HELP_TEXT)

    if verb_lower in {"보기", "주변", "봐", "look", "l"}:
        return CommandResult(world.describe_room(player.room_id))

    direction = DIRECTIONS.get(verb_lower) or DIRECTIONS.get(verb)
    if direction:
        room = world.rooms[player.room_id]
        if direction not in room.exits:
            return CommandResult("그 방향으로는 길이 없습니다.")
        player.room_id = room.exits[direction]
        return CommandResult(world.describe_room(player.room_id))

    if verb_lower in {"소지품", "인벤토리", "inventory", "inv", "i"}:
        if not player.inventory:
            return CommandResult("가진 물건이 없습니다.")
        names = [world.items[item_id].name for item_id in player.inventory if item_id in world.items]
        return CommandResult("가진 물건: " + ", ".join(names))

    if verb_lower in {"줍기", "집기", "get", "take"}:
        return CommandResult(_take_item(rest.strip(), player, world))

    if verb_lower in {"버리기", "drop"}:
        return CommandResult(_drop_item(rest.strip(), player, world))

    if verb_lower in {"상태", "status", "stat"}:
        return CommandResult(f"체력: {player.hp}/{player.max_hp}\r\n공격력: {player.attack}\r\n경험치: {player.exp}")

    if verb_lower in {"휴식", "쉬기", "rest"}:
        before = player.hp
        player.hp = min(player.max_hp, player.hp + 8)
        recovered = player.hp - before
        if recovered <= 0:
            return CommandResult("이미 충분히 회복했습니다.")
        return CommandResult(f"잠시 숨을 고릅니다. 체력을 {recovered} 회복했습니다.")

    if verb_lower in {"공격", "attack", "hit"}:
        return CommandResult(_attack_npc(rest.strip(), player, world))

    if verb_lower in {"말", "say", "'"}:
        text = rest.strip()
        if not text:
            return CommandResult("무엇을 말할까요?")
        spoken = f"{player.name}님이 말합니다: {text}"
        return CommandResult(f"당신이 말합니다: {text}", broadcast=spoken)

    if verb_lower in {"종료", "나가기", "quit", "exit"}:
        return CommandResult("퇴마요새에서 물러납니다. 진행 상태를 저장했습니다.", should_quit=True)

    return CommandResult("알 수 없는 명령입니다. '도움말'을 입력해 보세요.")


def _find_item_id(query: str, candidates: list[str], world: World) -> str | None:
    if not query:
        return None
    lowered = query.lower()
    for item_id in candidates:
        item = world.items.get(item_id)
        if item and (lowered == item_id.lower() or lowered == item.name.lower()):
            return item_id
    return None


def _take_item(query: str, player: Player, world: World) -> str:
    room = world.rooms[player.room_id]
    item_id = _find_item_id(query, room.items, world)
    if item_id is None:
        return "그 물건은 여기에 없습니다."
    room.items.remove(item_id)
    player.inventory.append(item_id)
    return f"{world.items[item_id].name}을(를) 주웠습니다."


def _drop_item(query: str, player: Player, world: World) -> str:
    item_id = _find_item_id(query, player.inventory, world)
    if item_id is None:
        return "그 물건은 가지고 있지 않습니다."
    player.inventory.remove(item_id)
    world.rooms[player.room_id].items.append(item_id)
    return f"{world.items[item_id].name}을(를) 내려놓았습니다."


def _find_npc_id(query: str, candidates: list[str], world: World) -> str | None:
    if len(candidates) == 1 and not query:
        return candidates[0]
    lowered = query.lower()
    for npc_id in candidates:
        npc = world.npcs.get(npc_id)
        if npc and (lowered == npc_id.lower() or lowered == npc.name.lower() or lowered in npc.name.lower()):
            return npc_id
    return None


def _attack_npc(query: str, player: Player, world: World) -> str:
    room = world.rooms[player.room_id]
    npc_id = _find_npc_id(query, room.npcs, world)
    if npc_id is None:
        return "공격할 대상이 없습니다."

    npc = world.npcs[npc_id]
    lines = [f"{npc.name}을(를) 공격했습니다. {player.attack} 피해를 입혔습니다."]
    npc.hp = max(0, npc.hp - player.attack)
    if npc.hp <= 0:
        room.npcs.remove(npc_id)
        player.exp += npc.exp_reward
        lines.append(f"{npc.name}이(가) 물러났습니다. 경험치 {npc.exp_reward}을(를) 얻었습니다.")
        return "\r\n".join(lines)

    player.hp = max(0, player.hp - npc.attack)
    lines.append(f"{npc.name}이(가) 반격합니다. {npc.attack} 피해를 받았습니다.")
    if player.hp <= 0:
        player.hp = max(1, player.max_hp // 2)
        player.room_id = "gate"
        lines.append("의식을 잃고 요새 정문에서 깨어났습니다.")
    else:
        lines.append(f"남은 체력: {player.hp}/{player.max_hp}")
    return "\r\n".join(lines)
