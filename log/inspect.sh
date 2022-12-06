
#docker run -it -v /go/src/DeFog/configs:/mnt/configs -v /go/src/DeFog/assets:/mnt/assets -v /go/src/DeFog/results:/mnt/results --name darknet_1 darknet:1.0 ../scripts/execute.sh 0 0
#python3 get_inspect.py darknet_1
#docker rm -f darknet_1

container="darknet_"
for ((i=1;i<=5;i=i+1))
do
    cn="$container$i"
    docker run -it -v /go/src/DeFog/configs:/mnt/configs -v /go/src/DeFog/assets:/mnt/assets -v /go/src/DeFog/results:/mnt/results --name $cn darknet:1.0 ../scripts/execute.sh 0 0
    python3 get_inspect.py $cn
    docker rm -f $cn
    done

