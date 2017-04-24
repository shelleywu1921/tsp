#include <stdio.h>
#include <stdlib.h>

typedef struct node {
    double *xadj;
    int *neighbors;
    int deg;
} node;

typedef struct xgraph {
    int ncount;
    node *nodelist;
    double *x;
} xgraph;

#define EPS 0.001


int main (int ac, char **av);
static int build_graph (xgraph *G, int ncount, int ecount, int *elist,
    double *x);
static void compute_delta (xgraph *G, int cnt, int *cut, int *marks, 
    double *pdelta);
static void verify_comb (int Hcount, int *H, int nteeth, int *Tcount, int **T,
    int *marks);

int main (int ac, char **av)
{
    int rval = 0, ncount, ecount, i, j, ncomb, nteeth, k, Hcount, p, irhs;
    int *elist = (int *) NULL, *marks = (int *) NULL;
    int *H = (int *) NULL, **T = (int **) NULL, *Tcount = (int *) NULL;
    double *x = (double *) NULL, delta, lhs;
    xgraph G;
    FILE *xin = (FILE *) NULL, *combin = (FILE *) NULL;

    G.nodelist = (node *) NULL;

    if (ac < 3) {
        printf ("Usage: %s x_file comb_file\n", *av);
        rval = 1; goto CLEANUP;
    }
        
    xin = fopen (av[1], "r");
    if (!xin) {
        fprintf (stderr, "could not open %s for input\n", av[1]);
        rval = 1; goto CLEANUP;
    }

    fscanf (xin, "%d %d", &ncount, &ecount);
    elist = (int *) malloc (2 * ecount * sizeof(int));
    if (!elist) {
        fprintf (stderr, "out of memory: elist\n"); rval = 1; goto CLEANUP;
    }
    x = (double *) malloc (ecount * sizeof(double));
    if (!x) {
        fprintf (stderr, "out of memory: x\n"); rval = 1; goto CLEANUP;
    }
    for (i = 0; i < ecount; i++) {
        fscanf (xin, "%d %d %lf", &(elist[2*i]), &(elist[2*i+1]), &(x[i]));
    }
    fclose (xin);
    xin = (FILE *) NULL;

    rval = build_graph (&G, ncount, ecount, elist, x);
    if (rval) {
        fprintf (stderr, "build_graph failed\n");
        rval = 1; goto CLEANUP;
    }

    printf ("x-vector: %d nodes, %d edges\n", ncount, ecount);
    fflush (stdout);

    combin = fopen (av[2], "r");
    if (!combin) {
        fprintf (stderr, "could not open %s for input\n", av[2]);
        rval = 1; goto CLEANUP;
    }

    fscanf (combin, "%d", &ncomb);

    marks = (int *) malloc (ncount * sizeof(int));
    if (!marks) {
        fprintf (stderr, "out of memory for marks\n"); rval = 1; goto CLEANUP;
    }
    for (i = 0; i < ncount; i++) marks[i] = 0;
    
    for (k = 0; k < ncomb; k++) {
        fscanf (combin, "%d", &p);  nteeth = p-1;

        fscanf (combin, "%d", &Hcount);
        H = (int *) malloc (Hcount * sizeof(int));
        if (!H) {
            fprintf (stderr, "out of memory: H\n"); rval = 1; goto CLEANUP;
        }
        for (j = 0; j < Hcount; j++) fscanf (combin, "%d", &H[j]);

        T = (int **) malloc (nteeth * sizeof(int *));
        Tcount = (int *) malloc (nteeth * sizeof(int));

        for (i = 0; i < nteeth; i++) {
            fscanf (combin, "%d", &Tcount[i]);
            T[i] = (int *) malloc (Tcount[i] * sizeof(int));
            if (!T[i]) {
                fprintf (stderr, "out of memory: T[i]\n");
                rval = 1; goto CLEANUP;
            }
            for (j = 0; j < Tcount[i]; j++) fscanf (combin, "%d", &(T[i][j]));
        }

        fscanf (combin, "%d", &irhs);
        compute_delta (&G, Hcount, H, marks, &lhs);
        for (i = 0; i < nteeth; i++) {
            compute_delta (&G, Tcount[i], T[i], marks, &delta);
            lhs += delta;
        }
        printf ("rhs = %d, lhs = %f, violation = %f\n", 3*nteeth+1, lhs,
                                            (double) (3*nteeth+1) - lhs);
        fflush (stdout);

        verify_comb (Hcount, H, nteeth, Tcount, T, marks);

        free (H);
	for (i = 0; i < nteeth; i++) free (T[i]);
        free (T);
    }

    fclose (combin);
    combin = (FILE *) NULL;

CLEANUP:
    if (marks) free (marks);
    if (elist) free (elist);
    if (x) free (x);
    if (G.nodelist) {
        for (i = 0; i < G.ncount; i++) {
            if (G.nodelist[i].neighbors) free (G.nodelist[i].neighbors);
            if (G.nodelist[i].xadj) free (G.nodelist[i].xadj);
        }
        free (G.nodelist);
    }
    if (xin) fclose (xin);
    if (combin) fclose (combin);
    return rval;
}

static int build_graph (xgraph *G, int ncount, int ecount, int *elist,
        double *x)
{
    int rval = 0, i, a, b;
    node *n, *na, *nb;

    G->nodelist = (node *) malloc (ncount * sizeof (node));
    if (!G->nodelist) {
        fprintf (stderr, "out of memory: nodelist\n"); rval = 1; goto CLEANUP;
    }

    for (i = 0; i < ncount; i++) {
        G->nodelist[i].deg = 0;
        G->nodelist[i].neighbors = (int *) NULL;
        G->nodelist[i].xadj =  (double *) NULL;
    }

    for (i = 0; i < ecount; i++) {
        a = elist[2*i];
        b = elist[2*i+1];
        G->nodelist[a].deg++;
        G->nodelist[b].deg++;
    }

    for (i = 0; i < ncount; i++) {
        n = &(G->nodelist[i]);
        n->neighbors = (int *) malloc (n->deg * sizeof (int));
        n->xadj = (double *) malloc (n->deg * sizeof (double));
        n->deg = 0;
    }

    for (i = 0; i < ecount; i++) {
        a = elist[2*i];
        b = elist[2*i+1];
        na = &(G->nodelist[a]);
        nb = &(G->nodelist[b]);

        na->neighbors[na->deg] = b;
        na->xadj[na->deg] = x[i];
        nb->neighbors[nb->deg] = a;
        nb->xadj[nb->deg] = x[i];

        na->deg++;
        nb->deg++;
    }

    G->ncount = ncount;
    G->x = x;

CLEANUP:
    return rval;
}

static void compute_delta (xgraph *G, int cnt, int *cut, int *marks, 
        double *pdelta)
{
    int i, j;
    node *n;
    double delta = 0.0;

    for (i = 0; i < cnt; i++) marks[cut[i]] = 1;

    for (i = 0; i < cnt; i++) {
        n = &(G->nodelist[cut[i]]);
        for (j = 0; j < n->deg; j++) {
            if (marks[n->neighbors[j]] == 0) {
                delta += n->xadj[j];
            }
        }
    }
 
    for (i = 0; i < cnt; i++) marks[cut[i]] = 0;
    *pdelta = delta;
}


static void verify_comb (int Hcount, int *H, int nteeth, int *Tcount, int **T,
        int *marks)
{
    int i, k, incount, outcount;

    for (i = 0; i < Hcount; i++) marks[H[i]] = 1;
    for (k = 0; k < nteeth; k++) {
        incount = outcount = 0;
        for (i = 0; i < Tcount[k]; i++) {
            if (marks[T[k][i]]) incount++;
            else                outcount++;
        }
        if (incount == 0) {
            printf ("tooth misses the handle\n");  exit (1);
        }
        if (outcount == 0) {
            printf ("tooth is contained in the handle\n");  exit (1);
        }
    }
    for (i = 0; i < Hcount; i++) marks[H[i]] = 0;

    for (k = 0; k < nteeth; k++) {
        for (i = 0; i < Tcount[k]; i++)  {
            if (marks[T[k][i]] == 1) {
                printf ("teeth intersect\n"); exit (1);
            } else {
                marks[T[k][i]] = 1;
            }
        }
    }
    for (k = 0; k < nteeth; k++) {
        for (i = 0; i < Tcount[k]; i++) marks[T[k][i]] = 0;
    }
}
