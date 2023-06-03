const makeFloat64Buffer = (initial) => {
  const buffer = new ArrayBuffer(8);

  const float64 = new Float64Array(buffer);

  float64[0] = initial;

  return buffer;
};

const conceal = (string) => {
  const buffer = makeFloat64Buffer(NaN);

  const ints = new Int8Array(buffer);

  for (let i = 5; i >= 0; i--) {
    const letter = string[5 - i];

    ints[i] = letter ? letter.charCodeAt(0) : 0;
  }

  return new Float64Array(buffer)[0];
};

const extract = (number) =>
  Array.from(new Int8Array(makeFloat64Buffer(number)))
    .slice(0, 6)
    .reverse()
    .filter((i) => i > 0)
    .map((l) => String.fromCharCode(l))
    .join("");

const nan = conceal("secret");

console.log(extract(nan)); // secret
