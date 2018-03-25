---
title: "A Night with Kubernetes"
date: 2018-03-21T23:13:40+08:00
tags: [""]
draft: true
---


export KUBECONFIG=/etc/kubernetes/admin.conf

debug nodes: `kubectl describe node`

`TODO: write content` 

`kubeadm reset`

brew cask install minikube

YMMV: your mileage may vary

<p class="text-center">***</p>

*Outline:*

1. https://coreos.com/blog/what-is-kubernetes.html
2. https://www.digitalocean.com/community/tutorials/an-introduction-to-kubernetes
3. https://kubernetes.io/docs/tutorials/
4. docker vs kubernetes
5. when to use kubernetes
6. book about kubernetes (kubernetes up and running)
7. minikube: https://github.com/kubernetes/minikube
8. kubernetes built-in ui
9. https://aws.amazon.com/eks/
10. https://kubernetes.io/case-studies/
11. open-sourced by Google in 2014: http://www.developintelligence.com/blog/2017/02/kubernetes-actually-use/
12. https://hackernoon.com/lessons-learned-from-moving-my-side-project-to-kubernetes-c28161a16c69
13. https://medium.com/@Grigorkh/install-kubernetes-on-ubuntu-1ac2ef522a36
14. https://zihao.me/post/creating-a-kubernetes-cluster-from-scratch-with-kubeadm/

[^2]:https://kubernetes.io/docs/tutorials/kubernetes-basics/explore-intro/


kubectl expose deployment hello-world-nginx --type="NodePort" --port 80


https://github.com/kubernetes/dashboard
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/master/src/deploy/recommended/kubernetes-dashboard.yaml


kubectl proxy --address=0.0.0.0 --port=80 --accept-hosts='.' --accept-paths='.'

kubeadm join --token cdcbb6.edf7c907c72fa231 67.205.174.18:6443 --discovery-token-ca-cert-hash sha256:0c4dcfdd06557f002432efbbddc6c71dc46e72c07df623caac3ccd2bc591fe7b

eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJyZXBsaWNhc2V0LWNvbnRyb2xsZXItdG9rZW4taGpqMm4iLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoicmVwbGljYXNldC1jb250cm9sbGVyIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiZWVjYjYzMjEtMmRmYS0xMWU4LTljMjctNWUwMjIyNWI3YjBmIiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50Omt1YmUtc3lzdGVtOnJlcGxpY2FzZXQtY29udHJvbGxlciJ9.X2_EKKxLPabrark_4eWoNnLU7f773HGxvZJSiJROnI0yIQe6ez2ECdW8Va_we6Ns9bFAV92-o2oh8xi6RckKIEpyFbMT2eOy7DPkl1y7N3C2BvLnhEbbV8OvrXsfUhb9kk2y-62QjnIh-6dR8Ocg_gsQG68Kg4ydKLLsALKoJ8NwDVwK3PJtrV6tjcB04fvgWYzjOeFEKIRFCOhUdXDo9TYhUjli_DRADDCSfIzssIO6ouFnOgXJ5-arcehyrNeqW922geNYCd4JAbssrL2lqb5f_t5OS-N_-CBgOGEq1PqcvebEPuI3WZM67vxzm60WG4dYWoRPFKpAGiQDVf-XUA