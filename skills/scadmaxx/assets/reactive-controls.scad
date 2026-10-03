// Include, not use: parameters and their dependencies participate in this source.
@{group: "Detail", description: "Detail height", range: [1:1:10],
  hidden: !advanced, locked: readonly || $detail_lock,}
detail = 3;
