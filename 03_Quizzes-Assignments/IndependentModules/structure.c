struct x { int i; float f; };
int f(struct x X) { return X.i*X.i-((int)X.f); }
