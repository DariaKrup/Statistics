%   DATE 2018.08.02 
%   getYZSection.m 
%
%   Функция находит проекцию фигуры заданной в XZ на плоскость x = h
%
%   [in] inSet - фигура, заданная в XZ
%   [in] h - задает плоскость YZ 
%   [out] outSet - проекция фигуры на плоскость x = h

function outSet = find_section(inSet, h)
  outSet = [];
  isEmpty = 1;
  
  for i = 1 : size(inSet, 1)
    a = h / inSet(i, 1);
    
    if (a > 1)
      a = 1;
    elseif (a < -1)
      a = -1;
    end
    
    if (abs(sin( acos(a)) > 1.e-010))
        isEmpty = 0;
    end
    outSet(size(outSet, 1) + 1, :) = [inSet(i, 1) * sin( acos(a) ), inSet(i, 2)];
  end
  
  if isEmpty == 1
      outSet = [];
  else
      firstInd = 1;
      lastInd = size(outSet, 1);
      
      while (abs(outSet(firstInd, 1)) < 1e-010)
          firstInd = firstInd + 1;
      end
      while (abs(outSet(lastInd, 1)) < 1e-010)
          lastInd = lastInd - 1;
      end
      
      if (firstInd ~= 1) && (lastInd ~= size(outSet, 1))
          outSet = outSet(firstInd-1:lastInd+1, :);
          outSet = [outSet; outSet(1, :)];
          
          firstInd = 2;
          lastInd = size(outSet, 1) - 2;
      end
      
      tmpSet = [];
      
      for i = firstInd:lastInd
          if abs(outSet(i, 1)) > 1e-010
              tmpSet(size(tmpSet, 1)+1, :) = outSet(i, :);
          else
              if abs(outSet(i - 1, 1)) > 1e-010 || abs(outSet(i + 1, 1)) > 1e-010
                  tmpSet(size(tmpSet, 1)+1, :) = outSet(i, :);
              end
          end
      end
      
      
      if (firstInd ~= 1) && (lastInd ~= size(outSet, 1))
          tmpSet = [outSet(1, :); tmpSet; outSet(end-1:end, :)];
      end
      outSet = tmpSet;
  end
end
