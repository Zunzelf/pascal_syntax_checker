program deretfibonacci;
 type
  UkPolozka = ^Polozka;
  UkHodnota = ^Hodnota;
  TypUdaj = (typretez, typcele, typrealne, typlogik, typpole, typobjekt);
 
  VarZaznam = record
      case Uda9j: TypUdaj of        
        typretez:  (case retez: TypUdaj of
            typcele:   (celeng: word);
        ) 
        ;
        typcele:   (cele: word);
        typrealne: (realne: single);
        typlogik:  (logik: boolean);
        typpole:   (pole: UkHodnota);
        typobjekt: (objekt: UkPolozka);
     end
     ;
 Polozka = record
    Nazev: string;
    Hodn:  (askus, bakus);
    Dalsi: UkPolozka
 end;


 Hodnota = record
    Hodn:  VarZaznam;
    Dalsi: UkHodnota     
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
    writeln(a xor b);
    writeln;
    a := 'a';
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
	if not ( a > 2) or not (a > a + 0)  then
      writeln('a is less than 20' )
   	else
      writeln('a is not less than 20', a );
    writeln('value of a is : ', a);  
	writeln('Your grade is  ', grade );
    for b := 1 to a do
    	begin
		    c := d + c +d;
		    d :=f;
		    f :=c;
		    write(c);
		    write(' ');
    	end;
    readln;

end.