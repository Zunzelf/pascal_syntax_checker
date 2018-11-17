program deretfibonacci;
var a, b, c, d, f : integer;
begin
    writeln('Program Deret Fibonacci ');
    writeln;
    write('Masukkan Jumlah Deret : ');
    readln(a);
    write('Deret Fibonacci ');
    d := 0;
    f := 1;
    c := 0;
    for b := 1 to a do
    begin
    c := d + c;
    d :=f;
    f :=c;
    write(c);
    write(' ');
    end;
    readln;
end.