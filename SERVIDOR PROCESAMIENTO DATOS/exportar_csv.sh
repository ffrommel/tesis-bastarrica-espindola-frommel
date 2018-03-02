#!/bin/bash
# exportar_csv.sh

# Obtener valores pasados por parametro
cantidad_parametros=$#
archivo_salida=$1
db=$2
collection=$3
cantidad_fields=$4
declare -a fields
i=0
while [ $i -lt $cantidad_fields ]; do
	eval "fields[$i]=\${$[$i+5]}"
	i=$[$i+1]
done
#( IFS=$'\n'; echo "${fields[*]}" ) # imprimir contenido array
eval "cantidad_querys=\${$[$cantidad_fields+5]}"
declare -a params
# menor		-> lt
# menor o igual	-> lte
# igual		-> eq
# mayor o igual	-> gte
# mayor		-> gt
# distinto	-> ne
declare -a conds
declare -a valores
i=0
j=0
while [ $i -lt $[$cantidad_querys*3] ]; do
	ind=$[$cantidad_fields+$i+6]
	eval "params[$j]=\${$[$ind]}"
	eval "conds[$j]=\${$[$ind+1]}"
	eval "valores[$j]=\${$[$ind+2]}"
	i=$[$i+3]
	j=$[$j+1]
done
#( IFS=$'\n'; echo "${params[*]}" )
#( IFS=$'\n'; echo "${conds[*]}" )
#( IFS=$'\n'; echo "${valores[*]}" )

# Armar comando
fields="${fields[@]}"
lista_fields=${fields// /,}
comando="mongoexport --db $db 
	--collection $collection 
	--out $archivo_salida --csv
	--fields $lista_fields
	--sort {\"event.timeStamp\":1}"

if [ $cantidad_querys -gt 0 ]; then
	comando="$comando --query {"
	i=0
	while [ $i -lt $cantidad_querys ]; do
		comando="$comando\"${params[$i]}\":{\$${conds[$i]}:${valores[$i]}}"
		if [ $i -lt $[$cantidad_querys - 1] ]; then # No es la ultima
			comando="$comando,"
		else # Es la ultima
			comando="$comando}"
		fi
		i=$[$i+1]
	done
fi
echo
echo $comando # imprimir comando
echo
$comando
