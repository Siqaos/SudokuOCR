#include<bits/stdc++.h>
using namespace std;
int tab[10][10];
bool RowCondition(int i,int j,int num){
	for(int indx=0;indx<9;indx++){
		if(num==tab[i][indx])
			return false;
	}
	return true;
}

bool ColCondition(int i,int j,int num){
	for(int indx=0;indx<9;indx++){
		if(num==tab[indx][j])
			return false;
	}
	return true;
}
bool subSquareCondition(int x,int y,int num){
	int startRow = ((x/3)*3)  , startCol = ((y/3)*3);
	for(int i=startRow;i<startRow+3;i++)
		for(int j=startCol;j<startCol+3;j++)
			if(tab[i][j]==num)
				return false;
	return true;
}
bool valide(int x,int y,int num){
	return RowCondition(x,y,num)&&ColCondition(x,y,num)&&subSquareCondition(x,y,num);
}

bool Solve(){
	for(int i=0;i<9;i++){
		for(int j=0;j<9;j++){
			if(tab[i][j]==0){
				for(int num=1;num<=9;num++){
					if(valide(i,j,num)){
						tab[i][j]=num;
						if(Solve())
							return true;
						tab[i][j]=0;
					}
				}
				return false;
			}
		}
	}

}


int main(){
	ios::sync_with_stdio(false);
	cin.tie(0);
	cout.tie(0);

	for(int i=0;i<9;i++)
		for(int j=0;j<9;j++)
			cin>>tab[i][j];

	if(Solve()){
		cout<<"+------+------+------+"<<endl;
		for(int i=0;i<9;i++){
			for(int j=0;j<9;j++){
				if(j%3==0)
					cout<<"|";
				cout<<tab[i][j]<<' ';
				if(j==8)
					cout<<'|';
			}
			if((i+1)%3==0)
				cout<<endl<<"+------+------+------+"<<endl;
			else
				cout<<endl;
		}
	}
	else{
		cout<<"Their is no Solution "<<endl;
	}


	return 0;
}