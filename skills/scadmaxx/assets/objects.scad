// Requires ordinary OEP8 object literals and object-function support.
base = {width:10, "label text":"cube",};
updated = object(base, width=20);
generated = {for(i=[1:3]) (str("n",i)):i*i};
combined = {each base, if(true) extra:42, let(x=3) triple:x*3};
assert(base.width == 10 && base["label text"] == "cube");
assert(object(width=10)["width"] == base.width);
assert(updated.width == 20 && base.width == 10);
assert(generated.n3 == 9 && combined.extra == 42 && combined.triple == 9);
assert(len({}) == 0);
echo("OBJECTS_PASS");
cube(updated.width);
