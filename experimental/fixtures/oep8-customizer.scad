base = {width: 10, "label text": "cube",};
assert(base.width == 10);
assert(base["label text"] == "cube");
assert(object(width=10)["width"] == base.width);
updated = object(base, width=20);
assert(updated.width == 20 && base.width == 10);
generated = {for (i=[1:3]) (str("n",i)): i*i};
assert(generated.n3 == 9);
combined = {each base, if (true) extra: 42, let(x=3) triple: x*3};
assert(combined.width == 10 && combined.extra == 42 && combined.triple == 9);
assert(len({}) == 0);
@{group: "Geometry", range: [1:100], hidden: false, locked: false,}
size = 10;
assert(size == 10);
echo("OEP8_AND_ANNOTATIONS_PASS");
cube(size);
