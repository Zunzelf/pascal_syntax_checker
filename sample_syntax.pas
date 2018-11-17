program deretfibonacci;
type 
	Books = record
	   title:  array ['1'..'50'] of char;
	   author: array [1..50] of char;
	   subject: array [1..100] of char;
	   book_id: integer;
	end;
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
    case (grade) of
      'A' : writeln('Excellent!' );
      'B', 'C': writeln('Well done' );
      'D' : writeln('You passed' );
      'F' : writeln('Better try again' );
	end;     
	if( (a < 20) or (a = 20)) then
      writeln('a is less than 20' )
   
   	else
      writeln('a is not less than 20' );
    writeln('value of a is : ', a);  
	writeln('Your grade is  ', grade );
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