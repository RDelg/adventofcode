from dataclasses import dataclass, field
from enum import Enum


EXAMPLE = """\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""


class Commands(str, Enum):
    cd = "cd"
    ls = "ls"


@dataclass
class File:
    name: str
    size: int


@dataclass
class Directory:
    name: str
    files: list[File] = field(default_factory=list)
    subdirs: dict[str, "Directory"] = field(default_factory=dict)
    parent: "Directory" = None

    def add_new_file(self, name: str, size: int) -> None:
        self.files.append(File(name, size))

    def add_new_subdir(self, name: str) -> None:
        self.subdirs[name] = Directory(name, parent=self)

    def update(
        self,
        command: Commands,
        current_position: int,
        data: list[str],
        args: list[str],
    ) -> "Directory":
        i = current_position
        if command == Commands.ls:
            next_line = data[i + 1]
            i += 1
            while not next_line.startswith("$ "):
                if next_line.startswith("dir "):
                    dir_name = next_line[4:]
                    self.add_new_subdir(dir_name)
                else:
                    size, name = next_line.split()
                    self.add_new_file(name, int(size))
                i += 1
                if i > len(data) - 1:
                    break
                next_line = data[i]
            return self, i - 1

        elif command == Commands.cd:
            dir_name = args[0]
            if dir_name == "..":
                return self.parent, i
            return self.subdirs[dir_name], i
        else:
            print("line", i, "is not a valid command", data[i])

    def __repr__(self) -> str:
        return f"Directory({self.name}, {self.files}, {self.subdirs})"

    def __getitem__(self, key: str) -> "Directory":
        return self.subdirs[key]

    def get_size(self) -> int:
        return sum(file.size for file in self.files) + sum(
            subdir.get_size() for subdir in self.subdirs.values()
        )

    def get_size_tree(self) -> dict[str, int]:
        return {
            self.name: self.get_size(),
            **{k: v.get_size_tree() for k, v in self.subdirs.items()},
        }

    def get_all_files(self) -> list[File]:
        return self.files


def flatten(d, parent_key="", sep="_"):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def part_1(data: str) -> int:
    root = Directory("/")
    lines = data.splitlines()[1:]
    cwd = root
    i = 0
    while i < len(lines) - 1:
        line = lines[i]
        cmd, *args = line[2:].split()
        cwd, i = cwd.update(command=cmd, current_position=i, data=lines, args=args)
        i += 1

    size_tree = root.get_size_tree()
    flat_size_tree = flatten(size_tree)
    return sum([x for x in flat_size_tree.values() if x < 100_000])


def part_2(data: str) -> int:

    root = Directory("/")
    lines = data.splitlines()[1:]
    cwd = root
    i = 0
    while i < len(lines) - 1:
        line = lines[i]
        cmd, *args = line[2:].split()
        cwd, i = cwd.update(command=cmd, current_position=i, data=lines, args=args)
        i += 1

    size_tree = root.get_size_tree()
    flat_size_tree = flatten(size_tree)
    TOTAL_SIZE = 70_000_000
    NEEDED_SIZE = 30_000_000

    to_free = root.get_size() - (TOTAL_SIZE - NEEDED_SIZE)

    sorted_dirs = sorted(flat_size_tree.values())
    for i in range(len(sorted_dirs)):
        if sorted_dirs[i] >= to_free:
            return sorted_dirs[i]


if __name__ == "__main__":
    # data
    with open("data/07.txt") as f:
        data = f.read()
    # part 1
    assert part_1(EXAMPLE) == 95437
    print("Part 1:", part_1(data))
    # part 2
    assert part_2(EXAMPLE) == 24933642
    print("Part 2:", part_2(data))
