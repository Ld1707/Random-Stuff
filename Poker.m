cards = 1:52;
cards = reshape(cards,[4,13]);

shuffle = round(1 + 51.*rand([4,13]));

for x = 1:52
    hold = x;
    swap = round(1 + 51.*rand([4,13]));
    cards(x) = cards(swap);
    cards(swap) = hold;
end