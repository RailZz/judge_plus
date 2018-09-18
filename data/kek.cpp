#include <iostream>
#include <cmath>
#include <vector>
using namespace std;
int main ()
{
	int N, M, a, b, kol1;
	cin >> N >> M;
	vector < vector<int> > gr(N);
	vector <int> G1;
	vector <int> G2;
	vector < vector<int> > kol(N, vector <int> (2));
	for (int i=0;i<M;i++)
	{
		cin >> a >> b;
		gr[a-1].push_back(b-1);
		gr[b-1].push_back(a-1);
	}
	for (int i=0;i<N;i++)
	{
		for (int j=0;j<G1.size();j++)
		{
			for (int z=0;z<gr[i].size();z++)
			{
				if (G1[j]==gr[i][z]+1)
				{
					kol[i][0]++;
				}
			}
		}
		if (kol[i][0]==0)
			G1.push_back(i+1);
		else
		{
			for (int i2=i;i2<N;i2++)
			{
				for (int j2=0;j2<G2.size();j2++)
				{
					for (int z2=0;z2<gr[i2].size();z2++)
					{
						if (G2[j2]==gr[i2][z2]+1)
							kol[i2][1]++;
					}
				}
				if (kol[i2][1]==0)
				{
					G2.push_back(i2+1);
				}
				if (kol[i2][1]>=1&&kol[i2][0]>=1)
				{
					kol1++;
					break;
				}
			}
		}
		if (kol1>2)
			break;
	}
	if (kol1==1)
		cout << "NO";
	if (kol1==0)
	{
		cout << "YES" << endl;
		for (int i=0;i<min(G1.size(),G2.size());i++)
		{
			if (G1.size()<G2.size())
				cout << G1[i] << " ";
			else
				cout << G2[i] << " ";
		}
	}
}