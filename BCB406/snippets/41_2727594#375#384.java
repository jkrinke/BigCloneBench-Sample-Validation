public Matrix transpose() {
    Matrix X = new Matrix ( n, m );
    double[][] C = X.getArray();
    for ( int i = 0; i < m; i++ ) {
        for ( int j = 0; j < n; j++ ) {
            C[j][i] = A[i][j];
        }
    }
    return X;
}
