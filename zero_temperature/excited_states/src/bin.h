#ifndef BINIO_H
#define BINIO_H

#include <iostream>

template <class T> static void
bwrite( ofstream& os, T** mat, int m, int n ) {
    for ( int i = 1; i <= m; ++i ) 
    {
	os.write( (const char*)(mat[i]+1), n*sizeof(T) );
    }
}

template <class T> static inline void
bwrite( ofstream& os, const T* data, int n ) {
	os.write( (const char *)(data+1), n * sizeof(T) );
}

template <class T> static inline void
bread( ifstream& is, T* data, int n ) {
	is.read( (char *)(data+1), n * sizeof(T) );
}

template <class T> static inline void
bwrite( ofstream& os, const T& x ) {
	os.write( (const char *)&x, sizeof(T) );
}

template <class T> static inline void 
bread( ifstream& is, T& x ) {
	is.read( (char *)&x, sizeof(T) );
}

template <class T> static void
bread( ifstream& is, T** mat, int m, int n ) 
{
    for ( int i = 1; i <= m; ++i ) 
    {
	is.read( (char *)(mat[i]+1), n * sizeof(T) );
    }
}


#endif
