#include<vcg/complex/complex.h>

#include <vcg/complex/algorithms/clustering.h>

#include <wrap/io_trimesh/import.h>
#include <wrap/io_trimesh/export.h>

class MyFace;
class MyVertex;

struct MyUsedTypes : public vcg::UsedTypes<	vcg::Use<MyVertex>::AsVertexType, vcg::Use<MyFace>::AsFaceType> {};

class MyVertex : public vcg::Vertex< MyUsedTypes, vcg::vertex::Coord3f, vcg::vertex::Normal3f, vcg::vertex::BitFlags  > {};
class MyFace : public vcg::Face < MyUsedTypes, vcg::face::VertexRef, vcg::face::Normal3f, vcg::face::BitFlags > {};
class MyMesh : public vcg::tri::TriMesh< std::vector<MyVertex>, std::vector<MyFace> > {};

using namespace vcg;
using namespace std;
int main()
{
	MyMesh m;
	vcg::tri::io::ImporterPLY<MyMesh>::Open(m, "segment7.ply");
	cout << m.vn;
	MyMesh segment[8];
	Point3f sum[8];
	int vertCount[8] ;
	Point3f s(0,0,0);
	for (int i = 0; i < m.vn; i++)
	{
		s = s + m.vert[i].cP();
	}
	s = s / m.vn;
	vcg::tri::UpdatePosition<MyMesh>::Translate(m,-s);

	for (int i = 0; i < 8; i++)
	{
		sum[i].X() = 0;
		sum[i].Y() = 0;
		sum[i].Z() = 0;
		vertCount[i] = 0;
	}
	for (int i = 0; i < m.vn; i++)
	{
		float x = m.vert[i].cP().X();
		float y = m.vert[i].cP().Y();
		float z = m.vert[i].cP().Z();
		cout << endl << x << y << z;

		if ((x > 0) && (y > 0) && (z > 0))
		{
			tri::Allocator<MyMesh>::AddVertex(segment[0], m.vert[i].cP());
			//segment[0].vert.push_back(m.vert[i]);
			sum[0].X() += x;
			sum[0].Y() += y;
			sum[0].Z() += z;
			vertCount[0]++;
		}
		if ((x > 0) && (y > 0) && (z < 0))
		{
			tri::Allocator<MyMesh>::AddVertex(segment[1], m.vert[i].cP());
			//segment[1].vert.push_back(m.vert[i]);
			sum[1].X() += x;
			sum[1].Y() += y;
			sum[1].Z() += z;
			vertCount[1]++;
		}
		if ((x > 0) && (y < 0) && (z > 0))
		{
			tri::Allocator<MyMesh>::AddVertex(segment[2], m.vert[i].cP());
			//segment[2].vert.push_back(m.vert[i]);
			sum[2].X() += x;
			sum[2].Y() += y;
			sum[2].Z() += z;
			vertCount[2]++;
		}

		if ((x > 0) && (y < 0) && (z < 0))
		{
			tri::Allocator<MyMesh>::AddVertex(segment[3], m.vert[i].cP());
			//segment[3].vert.push_back(m.vert[i]);
			sum[3].X() += x;
			sum[3].Y() += y;
			sum[3].Z() += z;
			vertCount[3]++;
		}


		if ((x < 0) && (y > 0) && (z > 0))
		{
			tri::Allocator<MyMesh>::AddVertex(segment[4], m.vert[i].cP());
			//segment[4].vert.push_back(m.vert[i]);
			sum[4].X() += x;
			sum[4].Y() += y;
			sum[4].Z() += z;
			vertCount[4]++;
		}
		if ((x < 0) && (y > 0) && (z < 0))
		{
			tri::Allocator<MyMesh>::AddVertex(segment[5], m.vert[i].cP());
			//segment[5].vert.push_back(m.vert[i]);
			sum[5].X() += x;
			sum[5].Y() += y;
			sum[5].Z() += z;
			vertCount[5]++;
		}
		if ((x < 0) && (y < 0) && (z > 0))
		{
			tri::Allocator<MyMesh>::AddVertex(segment[6], m.vert[i].cP());
			//segment[6].vert.push_back(m.vert[i]);
			sum[6].X() += x;
			sum[6].Y() += y;
			sum[6].Z() += z;
			vertCount[6]++;
		}

		if ((x < 0) && (y < 0) && (z < 0))
		{
			tri::Allocator<MyMesh>::AddVertex(segment[7], m.vert[i].cP());
			//segment[7].vert.push_back(m.vert[i]);
			sum[7].X() += x;
			sum[7].Y() += y;
			sum[7].Z() += z;
			vertCount[7]++;
		}
	}
	MyMesh output;
	for( int i =0; i<8 ;i++)
		vcg::tri::io::ExporterPLY<MyMesh>::Save(segment[i], (std::to_string(i)+".ply").c_str());

	for (int i = 0; i < 8; i++)
	{
		sum[i] = Point3f(0,0,0);//sum[i]/vertCount[i];
	}

	for (int i = 0; i < 8; i++)
		vcg::tri::UpdatePosition<MyMesh>::Translate(segment[i], -sum[i]);

	for (int i = 0; i < 8; i++)
	{
		
		float max = 0; int index = 0;
		for (int j = 0; j < segment[i].vn; j++)
		{
			float x = segment[i].vert[j].cP().X();
			float y = segment[i].vert[j].cP().Y();
			float z = segment[i].vert[j].cP().Z();
			float d = x*x + y*y + z*z;
			if (d > max)
			{
				max = d;
				index = j;
			}
		}
		if (segment[i].vn > 0)
		{
			Point3f maxP = segment[i].vert[index].cP() + sum[i] + s;
			std::cout << maxP.X() << "  " << maxP.Y() << "  " << maxP.Z();
			tri::Allocator<MyMesh>::AddVertex(output, maxP);
		}
			
	}	
	std::string outputFileName = "output.ply";
	vcg::tri::io::ExporterPLY<MyMesh>::Save(output, outputFileName.c_str());

	for (int i = 0; i < 8; i++)
	{
		vcg::tri::UpdatePosition<MyMesh>::Translate(segment[i], s);
		vcg::tri::io::ExporterPLY<MyMesh>::Save(segment[i], ("segment"+std::to_string(i) + ".ply").c_str());
	}
		
}