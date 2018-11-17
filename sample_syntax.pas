program deretfibonacci;
var a, b, c, d, f : integer;
procedure findMin(x, y, z: integer; var m: integer);
	begin
	   if x < y then
	      m := x
	   else
	      m := y;
	   
	   if z <m then
	      m := z;
	end;
function fibonacci(n: integer; n: integer): integer;
	begin
	   if n=1 then
	      fibonacci := 0
	   
	   else if n=2 then
	      fibonacci := 1
	   
	   else
	      fibonacci := fibonacci(n-1) + fibonacci(n-2);
	end; 	
procedure findMin(x, y, z: integer; var m: integer);
	begin
	   if x < y then
	      m := x
	   else
	      m := y;
	   
	   if z <m then
	      m := z;
	end;
begin
    writeln(20, 20);
    writeln;
    write('Masukkan Jumlah Deret : ');
    readln(a);
    write('Deret Fibonacci ');
    d := 0.0;
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